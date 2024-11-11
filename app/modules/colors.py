from typing import Dict, List
import numpy as np
from numpy.typing import NDArray
import nfl_data_py as nfl
from app.models.animation_types import TeamColors

class ColorManager:
    def __init__(self) -> None:
        self._colors: Dict[str, List[str]] = {
    "ARI": ["#97233F", "#000000", "#FFB612"],
    "ATL": ["#A71930", "#000000", "#A5ACAF"],
    "BAL": ["#241773", "#000000"],
    "BUF": ["#00338D", "#C60C30"],
    "CAR": ["#0085CA", "#101820", "#BFC0BF"],
    "CHI": ["#0B162A", "#C83803"],
    "CIN": ["#FB4F14", "#000000"],
    "CLE": ["#311D00", "#FF3C00"],
    "DAL": ["#003594", "#041E42", "#869397"],
    "DEN": ["#FB4F14", "#002244"],
    "DET": ["#0076B6", "#B0B7BC", "#000000"],
    "GB": ["#203731", "#FFB612"],
    "HOU": ["#03202F", "#A71930"],
    "IND": ["#002C5F", "#A2AAAD"],
    "JAX": ["#101820", "#D7A22A", "#9F792C"],
    "KC": ["#E31837", "#FFB81C"],
    "LA": ["#003594", "#FFA300", "#FF8200"],
    "LAC": ["#0080C6", "#FFC20E", "#FFFFFF"],
    "LV": ["#000000", "#A5ACAF"],
    "MIA": ["#008E97", "#FC4C02", "#005778"],
    "MIN": ["#4F2683", "#FFC62F"],
    "NE": ["#002244", "#C60C30", "#B0B7BC"],
    "NO": ["#101820", "#D3BC8D"],
    "NYG": ["#0B2265", "#A71930", "#A5ACAF"],
    "NYJ": ["#125740", "#000000", "#FFFFFF"],
    "PHI": ["#004C54", "#A5ACAF", "#ACC0C6"],
    "PIT": ["#FFB612", "#101820"],
    "SEA": ["#002244", "#69BE28", "#A5ACAF"],
    "SF": ["#AA0000", "#B3995D"],
    "TB": ["#D50A0A", "#FF7900", "#0A0A08"],
    "TEN": ["#0C2340", "#4B92DB", "#C8102E"],
    "WAS": ["#5A1414", "#FFB612"],
    "football": ["#CBB67C", "#663831"],
        }
        self.teams = nfl.import_team_desc()
        self.team_colors = self.teams.set_index("team_abbr")[
            ["team_color", "team_color2", "team_color3", "team_color4"]
        ].to_dict(orient="index")

    def hex_to_rgb(self, hex_color: str) -> NDArray[np.int_]:
        """Convert hex color to RGB array."""
        return np.array(
            tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        )

    def calculate_color_distance(self, hex1: str, hex2: str) -> float:
        """Calculate the perceptual distance between two colors."""
        if hex1 == hex2:
            return 0.0
        
        rgb1 = self.hex_to_rgb(hex1)
        rgb2 = self.hex_to_rgb(hex2)
        rm = 0.5 * (rgb1[0] + rgb2[0])
        weights = np.array([2 + rm, 4, 3 - rm])
        
        return float(np.sqrt(np.sum(weights * (rgb1 - rgb2) ** 2)))

    def get_team_colors(self, team: str) -> List[str]:
        """Get color scheme for a team."""
        return self._colors.get(team, ["#FFFFFF", "#000000"])

    def get_contrasting_pairs(self, team1: str, team2: str) -> Dict[str, List[str]]:
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
