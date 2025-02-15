from flask import Flask, render_template, request, jsonify
import requests
import spacy
import re
from datetime import datetime, timedelta

# Initialize spaCy NLP model
nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

API_KEY = 'ff779e34028545f08691036d8733d1e2' 
# Helper function to fetch data from Football-Data API
def get_soccer_data(endpoint, params=None):
    url = f'https://api.football-data.org/v4/{endpoint}'
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        
        if 'scorers' in data:
            for scorer in data['scorers']:
                scorer['goals'] = scorer.get('goals', 0)  # Default to 0 if no goals are found

        
        if 'matches' in data:
            for match in data['matches']:
                if not match.get('score') or not match['score'].get('fullTime'):
                    match['score'] = {
                        'fullTime': {
                            'homeTeam': 0,
                            'awayTeam': 0
                        }
                    }

        return data
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}


# NLP function to parse queries and extract relevant information
def parse_query(user_query):
    doc = nlp(user_query.lower())
    league = None
    player = None
    match_query = False
    past_match_query = False
    year = None

    # List of league names (including multi-word names)
    league_names = [
        'premier league', 'premier',
        'la liga',
        'bundesliga',
        'serie a',
        'ligue 1',
        'champions league',
        'world cup',
        'eredivisie',
        'brasileirao',
        'championship',
        'primeira liga',
        'european championship',
        'copa libertadores'
    ]

    # Extract relevant entities and dates from the query
    for ent in doc.ents:
        if ent.label_ == "DATE" and re.match(r'\b(19|20)\d{2}\b', ent.text):
            year = ent.text
        if ent.label_ == "PERSON":
            player = ent.text

    # Check for league names in the user query
    for league_name in league_names:
        if league_name in user_query.lower():
            league = league_name
            break

    # Extract tokens for match details
    for token in doc:
        if token.text in ['match', 'matches', 'result', 'schedule', 'upcoming']:
            match_query = True
        if token.text in ['yesterday', 'past', 'last', 'previous']:
            past_match_query = True

    return league, player, year, match_query, past_match_query


@app.route('/')
def home():
    return render_template('soccer_bot.html')


@app.route('/get-data', methods=['POST'])
def get_data():
    user_query = request.json.get('query', '')

    # Parse query using NLP
    league, player, year, match_query, past_match_query = parse_query(user_query)

    # Handle player stats
    if player:
        if league:
            league_code = get_league_code(league)
            if league_code:
                player_stats = get_player_stats(league_code, player)
                return jsonify(player_stats)
            else:
                return jsonify({"error": "League not recognized."})
        else:
            return jsonify({"error": "Please specify a league for player stats."})

    # Handle match queries (upcoming or past)
    if match_query:
        if league:
            league_code = get_league_code(league)
            if league_code:
                matches = get_matches(league_code, year, past_match_query)
                return jsonify(matches)
            else:
                return jsonify({"error": "League not recognized."})
        else:
            return jsonify({"error": "Please specify a league for match queries."})

    # Handle top scorers and standings
    if "top scorer" in user_query.lower() or "top scorers" in user_query.lower():
        if league:
            league_code = get_league_code(league)
            if league_code:
                scorers = get_soccer_data(f'competitions/{league_code}/scorers', params={'season': year})
                return jsonify(scorers)
            else:
                return jsonify({"error": "League not recognized."})
        else:
            return jsonify({"error": "Please specify a league for top scorers."})

    # Default to standings query
    if league:
        league_code = get_league_code(league)
        if league_code:
            standings = get_soccer_data(f'competitions/{league_code}/standings', params={'season': year})
            return jsonify(standings)
        else:
            return jsonify({"error": "League not recognized."})

    return jsonify({"error": "Could not identify the league or entity."})


# Helper function to get league code from the league name
def get_league_code(league):
    league_codes = {
        'premier league': 'PL',
        'premier': 'PL',
        'la liga': 'PD',
        'bundesliga': 'BL1',
        'serie a': 'SA',
        'ligue 1': 'FL1',
        'champions league': 'CL',
        'world cup': 'WC',
        'eredivisie': 'DED',
        'brasileirao': 'BSA',
        'championship': 'ELC',
        'primeira liga': 'PPL',
        'european championship': 'EC',
        'copa libertadores': 'CLI'
    }
    return league_codes.get(league)


# Helper function to get player stats
def get_player_stats(league_code, player_name):
    # Fetch team rosters and find the player (as API doesn't allow querying players directly by name)
    roster = get_soccer_data(f'competitions/{league_code}/teams')
    if 'teams' in roster:
        for team in roster['teams']:
            players = get_soccer_data(f'teams/{team["id"]}/players')
            for p in players.get('players', []):
                if player_name.lower() in p['name'].lower():
                    return {
                        'player': p['name'],
                        'team': team['name'],
                        'matches': p.get('appearances', 'N/A'),
                        'goals': p.get('goals', 'N/A'),
                        'assists': p.get('assists', 'N/A')
                    }
    return {"error": "Player not found."}


# Helper function to get matches (upcoming or past)
def get_matches(league_code, year, past=False):
    # Set the appropriate date range for past or upcoming matches
    if past:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        params = {'dateFrom': yesterday, 'dateTo': yesterday}
    else:
        params = {'status': 'SCHEDULED'} if not year else {'season': year}

    matches = get_soccer_data(f'competitions/{league_code}/matches', params=params)

    # Check if matches are found, and if not, return an error
    if 'matches' in matches:
        for match in matches['matches']:
            # Ensure that future matches show '0 - 0' as score if they have not been played yet
            if match.get('score') and match['score'].get('fullTime'):
                # Extract scores from the fullTime object if available
                fullTime = match['score']['fullTime']
                match['score_display'] = {
                    'homeTeam': fullTime.get('homeTeam', 0),
                    'awayTeam': fullTime.get('awayTeam', 0)
                }
            else:
                # Set default score to 0 - 0 for matches that haven't been played
                match['score_display'] = {
                    'homeTeam': 0,
                    'awayTeam': 0
                }
        return matches
    else:
        return {"error": "No matches found."}



if __name__ == '__main__':
    app.run(debug=True)
