document.addEventListener('DOMContentLoaded', function() {
    // Fetch populations and populate dropdowns
    fetch('/get_populations')
        .then(response => response.json())
        .then(populations => {
            const populationDropdowns = document.querySelectorAll('.population-dropdown');
            populationDropdowns.forEach(dropdown => {
                populations.forEach(population => {
                    const option = new Option(population.PopulationName, population.PopulationID);
                    dropdown.add(option);
                });
            });

            // Add event listener to the analyze button
            document.getElementById('analyze-btn').addEventListener('click', function(event) {
                event.preventDefault(); // Prevent default form submission
                var formData = {
                    populations: [] // Initialize an array to store selected populations
                };
                // Iterate over all selected options and add them to the formData array
                var selectedOptions = dropdown.selectedOptions;
                for (var i = 0; i < selectedOptions.length; i++) {
                    formData.populations.push(selectedOptions[i].value);
                }

                // AJAX request
                fetch('/analyze_admixture', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => response.json())
                .then(response => {
                    console.log('Analysis Results:', response); // Log response data
                    // Pass data to interactive_plot.js for chart rendering
                    renderChart(response);
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Handle error, e.g., display error message to user
                });
            });
        })
        .catch(error => console.error('Error fetching populations:', error));
});
