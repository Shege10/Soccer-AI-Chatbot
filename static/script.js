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

        // Extract the year from the query (optional if detected by the backend)
        let yearMatch = query.match(/\b(19|20)\d{2}\b/);  // Regex to find a 4-digit year
        let year = yearMatch ? yearMatch[0] : null;

        if (data.error) {
            responseDiv.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        // Show a message with the year if it exists
        if (year) {
            responseDiv.innerHTML += `<p>Showing results for the year ${year}:</p>`;
        }

        // Check if top scorers data is present
        if (data.scorers && data.scorers.length > 0) {
            // Create a table for top scorers
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

        } else if (data.standings) {
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
        } else {
            responseDiv.innerHTML = `<p>No valid data available for this query.</p>`;
        }
    })
    .catch(error => {
        let responseDiv = document.getElementById('response');
        responseDiv.innerHTML = `<p>There was an error processing your request: ${error.message}</p>`;
    });
});

// Add an event listener to the input field to detect the "Enter" key press
document.getElementById('queryInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // Prevent the default action (form submission)
        document.getElementById('sendBtn').click();  // Trigger the send button click
    }
});
