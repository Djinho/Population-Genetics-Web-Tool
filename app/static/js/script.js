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
        })
        .catch(error => console.error('Error fetching populations:', error));
});
