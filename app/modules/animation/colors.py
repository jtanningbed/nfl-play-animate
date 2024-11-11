from typing import Final, Self
import numpy as np
from numpy.typing import NDArray
import nfl_data_py as nfl
import pandas as pd

class ColorManager:
    FOOTBALL_COLORS: Final[list[str]] = ["#CBB67C", "#663831"]

    def __init__(self: Self) -> None:
        """Initialize the ColorManager with NFL team colors from nfl_data_py."""
        self.teams: pd.DataFrame = nfl.import_team_desc()
        team_colors_df: pd.DataFrame = self.teams.set_index("team_abbr")[
            ["team_color", "team_color2", "team_color3", "team_color4"]
        ]
        
        # Convert team colors to our format and add football colors
        self._colors: dict[str, list[str]] = {}
        for team in team_colors_df.index:
            colors = [
                f"#{color}" if color and not color.startswith("#") else color
                for color in team_colors_df.loc[team]
                if color and color.strip()
            ]
            if colors:  # Only add teams with at least one color
                self._colors[team] = colors

        # Add football colors
        self._colors["football"] = self.FOOTBALL_COLORS

    def hex_to_rgb(self: Self, hex_color: str) -> NDArray[np.int_]:
        """Convert hex color to RGB array."""
        return np.array(
            tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        )

    def calculate_color_distance(self: Self, hex1: str, hex2: str) -> float:
        """Calculate the perceptual distance between two colors."""
        if hex1 == hex2:
            return 0.0
        
        rgb1 = self.hex_to_rgb(hex1)
        rgb2 = self.hex_to_rgb(hex2)
        rm = 0.5 * (rgb1[0] + rgb2[0])
        weights = np.array([2 + rm, 4, 3 - rm])
        
        return float(np.sqrt(np.sum(weights * (rgb1 - rgb2) ** 2)))

    def get_team_colors(self: Self, team: str) -> list[str]:
        """Get color scheme for a team."""
        return self._colors.get(team, ["#FFFFFF", "#000000"])

    def get_contrasting_pairs(self: Self, team1: str, team2: str) -> dict[str, list[str]]:
        """Get contrasting color pairs for two teams."""
        color_array_1 = self.get_team_colors(team1)
        color_array_2 = self.get_team_colors(team2)
        
        if self.calculate_color_distance(color_array_1[0], color_array_2[0]) < 500:
            return {
                team1: [color_array_1[0], color_array_1[1]],
                team2: [color_array_2[1], color_array_2[0]],
                "football": self._colors["football"],
            }
        
        return {
            team1: [color_array_1[0], color_array_1[1]],
            team2: [color_array_2[0], color_array_2[1]],
            "football": self._colors["football"],
        }
