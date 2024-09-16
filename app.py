from flask import Flask, render_template, request, jsonify
import requests
import re  # For regex to detect the year in the user query

app = Flask(__name__)

# Function to fetch soccer data from the Football-Data API
def get_soccer_data(query, data_type='standings', year=None):
    API_KEY = 'ff779e34028545f08691036d8733d1e2'  # Replace with your valid API key

    # Add year as a query parameter if specified
    if year:
        url = f'https://api.football-data.org/v4/competitions/{query}/{data_type}?season={year}'
    else:
        url = f'https://api.football-data.org/v4/competitions/{query}/{data_type}'

    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-data', methods=['POST'])
def get_data():
    user_query = request.json.get('query', '').lower()
    
    # Extract the year from the user's query (if provided)
    year_match = re.search(r'\b(19|20)\d{2}\b', user_query)  # Look for a 4-digit year
    year = year_match.group(0) if year_match else None

    # Detect if the user is asking for top scorers
    if "top scorer" in user_query or "top scorers" in user_query:
        if "premier league" in user_query:
            data = get_soccer_data('PL', 'scorers', year)
        elif "la liga" in user_query:
            data = get_soccer_data('PD', 'scorers', year)
        elif "bundesliga" in user_query:
            data = get_soccer_data('BL1', 'scorers', year)
        elif "serie a" in user_query:
            data = get_soccer_data('SA', 'scorers', year)
        elif "ligue 1" in user_query:
            data = get_soccer_data('FL1', 'scorers', year)
        elif "fifa world cup" in user_query:
            data = get_soccer_data('WC', 'scorers', year)
        elif "champions league" in user_query:
            data = get_soccer_data('CL', 'scorers', year)
        elif "eredivisie" in user_query:
            data = get_soccer_data('DED', 'scorers', year)
        elif "brasileirao" in user_query or "campeonato brasileiro" in user_query:
            data = get_soccer_data('BSA', 'scorers', year)
        elif "championship" in user_query:
            data = get_soccer_data('ELC', 'scorers', year)
        elif "primeira liga" in user_query:
            data = get_soccer_data('PPL', 'scorers', year)
        elif "european championship" in user_query:
            data = get_soccer_data('EC', 'scorers', year)
        elif "copa libertadores" in user_query:
            data = get_soccer_data('CLI', 'scorers', year)
        else:
            data = {"error": "No data available for that query."}
    
    # Default to standings query if no top scorer keyword is found
    else:
        if "premier league" in user_query:
            data = get_soccer_data('PL', 'standings', year)
        elif "la liga" in user_query:
            data = get_soccer_data('PD', 'standings', year)
        elif "bundesliga" in user_query:
            data = get_soccer_data('BL1', 'standings', year)
        elif "serie a" in user_query:
            data = get_soccer_data('SA', 'standings', year)
        elif "ligue 1" in user_query:
            data = get_soccer_data('FL1', 'standings', year)
        elif "fifa world cup" in user_query:
            data = get_soccer_data('WC', 'standings', year)
        elif "champions league" in user_query:
            data = get_soccer_data('CL', 'standings', year)
        elif "eredivisie" in user_query:
            data = get_soccer_data('DED', 'standings', year)
        elif "brasileirao" in user_query or "campeonato brasileiro" in user_query:
            data = get_soccer_data('BSA', 'standings', year)
        elif "championship" in user_query:
            data = get_soccer_data('ELC', 'standings', year)
        elif "primeira liga" in user_query:
            data = get_soccer_data('PPL', 'standings', year)
        elif "european championship" in user_query:
            data = get_soccer_data('EC', 'standings', year)
        elif "copa libertadores" in user_query:
            data = get_soccer_data('CLI', 'standings', year)
        else:
            data = {"error": "No data available for that query."}
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
