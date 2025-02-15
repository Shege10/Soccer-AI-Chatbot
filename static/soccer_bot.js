document.getElementById('sendBtn').addEventListener('click', function() {
    let query = document.getElementById('queryInput').value;

    fetch('/get-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
    })
    .then(response => response.json())
    .then(data => {
        let responseDiv = document.getElementById('response');
        responseDiv.innerHTML = '';  // Clear the existing response

        if (data.error) {
            responseDiv.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        // Check if player stats are present
        if (data.player_stats) {
            let table = `<table border="1"><thead><tr><th>Player</th><th>Matches Played</th><th>Goals</th><th>Assists</th></tr></thead><tbody>`;
            table += `<tr><td>${data.player_stats.player}</td><td>${data.player_stats.matches}</td><td>${data.player_stats.goals}</td><td>${data.player_stats.assists}</td></tr>`;
            table += '</tbody></table>';
            responseDiv.innerHTML += table;
        }
        // Check if top scorers data is present
        else if (data.scorers && data.scorers.length > 0) {
            let table = `<table border="1"><thead><tr>
                <th>Position</th><th>Player</th><th>Team</th><th>Goals</th></tr></thead><tbody>`;

            // Loop through each scorer and populate the table
            data.scorers.forEach((scorer, index) => {
                table += `<tr>
                    <td>${index + 1}</td>
                    <td>${scorer.player.name}</td>
                    <td>${scorer.team.name}</td>
                    <td>${scorer.numberOfGoals || scorer.goals}</td>
                </tr>`;
            });

            table += '</tbody></table>';  // Close the table
            responseDiv.innerHTML += table;

        }
        // Check if standings data is present
        else if (data.standings) {
            // Create a table for standings
            let table = `<table border="1"><thead><tr>
                <th>Position</th><th>Team</th><th>Played</th><th>Won</th>
                <th>Drawn</th><th>Lost</th><th>Points</th></tr></thead><tbody>`;

            // Populate the standings table
            data.standings[0].table.forEach(team => {
                table += `<tr>
                    <td>${team.position}</td>
                    <td>${team.team.name}</td>
                    <td>${team.playedGames}</td>
                    <td>${team.won}</td>
                    <td>${team.draw}</td>
                    <td>${team.lost}</td>
                    <td>${team.points}</td>
                </tr>`;
            });

            table += '</tbody></table>';  // Close the table
            responseDiv.innerHTML += table;
        }
        // Check if match data (upcoming or past) is present
        else if (data.matches) {
            let table = `<table border="1"><thead><tr><th>Date</th><th>Home Team</th><th>Away Team</th><th>Score</th></tr></thead><tbody>`;

            data.matches.forEach(match => {
                // Check if the match is finished or if it's scheduled
                let score = '0 - 0'; // Default for scheduled matches
                if (match.status === 'FINISHED' && match.score && match.score.fullTime) {
                    let homeScore = match.score.fullTime.homeTeam !== null ? match.score.fullTime.homeTeam : 0;
                    let awayScore = match.score.fullTime.awayTeam !== null ? match.score.fullTime.awayTeam : 0;
                    score = `${homeScore} - ${awayScore}`;
                }

                // Convert match date to a readable format
                const matchDate = new Date(match.utcDate).toLocaleString();

                table += `<tr><td>${matchDate}</td><td>${match.homeTeam.name}</td><td>${match.awayTeam.name}</td><td>${score}</td></tr>`;
            });

            table += '</tbody></table>';
            responseDiv.innerHTML += table;
        }
        // Handle no valid data found
        else {
            responseDiv.innerHTML = '<p>No valid data available for this query.</p>';
        }
    })
    .catch(error => {
        let responseDiv = document.getElementById('response');
        responseDiv.innerHTML = `<p>There was an error processing your request: ${error.message}</p>`;
    });
});

// Event listener to the input field to detect the "Enter" key press
document.getElementById('queryInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // Prevent the default action (form submission)
        document.getElementById('sendBtn').click();  // Trigger the send button click
    }
});
