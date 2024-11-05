# NFL Play Animator

A simple web application to animate NFL plays using FastAPI and Streamlit.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/nfl-play-animate.git
   cd nfl-play-animate
   ```

2. **Set up a virtual environment using `uv`:**

   ```bash
   uv create
   ```

3. **Activate the virtual environment:**

   ```bash
   uv activate
   ```

4. **Install the dependencies:**

   ```bash
   uv install
   ```

## Setup

1. **Database Setup:**

   - Download the public NFL data from Kaggle and import it into a local PostgreSQL database.
   - Ensure you have PostgreSQL installed and running on your machine.
   - Create a new database and import the data into it.

2. **Environment Variables:**

   - Create a `.env` file in the root directory of the project with the following content:

     ```plaintext
     DB_USER=your_db_username
     DB_PASSWORD=your_db_password
     DB_NAME=your_db_name
     DB_HOSTNAME=localhost
     ```

   Replace `your_db_username`, `your_db_password`, and `your_db_name` with your actual database credentials.

## Running the Application

1. **Start the application using the Makefile:**

   ```bash
   make start
   ```

   This will start both the FastAPI server and the Streamlit app.

2. **Stop the application:**

   To stop the running services, use:

   ```bash
   make stop
   ```

## Usage

- Use the Streamlit interface to select a week, game, and play to animate.
- The app will fetch data from the FastAPI server and display an animation of the selected play.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Makefile

The `Makefile` includes the following commands:

- **start**: Runs both the FastAPI server and the Streamlit app.
- **stop**: Stops the running FastAPI server and Streamlit app.
