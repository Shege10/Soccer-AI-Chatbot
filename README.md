# Soccer-AI-Chatbot
The Soccer AI Chatbot is a Flask-based web app that uses NLP to provide real-time soccer data. It integrates with the Football-Data API to fetch match scores, player stats, league standings, and top scorers. Users can ask questions about teams, players, and matches for instant, accurate responses.
## Features

- **Player Stats:** Users can query player statistics (e.g., goals, assists, appearances) from various soccer leagues.
- **Match Information:** Get details on upcoming or past soccer matches based on a specified league and year.
- **Top Scorers:** Retrieve the list of top scorers for different leagues.
- **League Standings:** Get current standings for different soccer leagues.
- **Natural Language Processing (NLP):** The chatbot uses spaCy to parse user queries and extract meaningful information.

## Prerequisites

Before running the application, you need to install the following dependencies:

- Python 3.x
- Flask
- Requests
- spaCy
- Football-Data API key

### Install Dependencies

1. Ensure that you have Python 3.x installed.
2. Install the required dependencies by running:
    pip install -r requirements.txt
3. **Football-Data API Key:**  
   Obtain an API key from [Football-Data.org](https://www.football-data.org/) and replace the `API_KEY` variable in the `app.py` file with your API key.

### Run the Application

To start the Flask application, run the following command:
python app.py
