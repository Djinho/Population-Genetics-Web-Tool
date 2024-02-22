$(document).ready(function() {
    // Autocomplete for gene names
    $('#gene-name').autocomplete({
        source: '/autocomplete/gene_names',
        minLength: 2 // Trigger autocomplete with at least 2 characters
    });

    // Fetch populations and populate checkboxes on page load
    fetch('/get_populations')
        .then(response => response.json())
        .then(data => {
            const superPopulationContainer = document.querySelector('.superpopulation-checkbox-group');
            const populationContainer = document.querySelector('.population-checkbox-group');

            // Populate superpopulations
            data.superpopulations.forEach(spop => {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'superpopulations';
                checkbox.value = spop.PopulationID;

                const label = document.createElement('label');
                label.textContent = spop.PopulationName + ' (Superpopulation)';
                label.insertBefore(checkbox, label.firstChild);

                superPopulationContainer.appendChild(label);
            });

            // Populate populations
            data.populations.forEach(pop => {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'populations';
                checkbox.value = pop.PopulationID;

                const label = document.createElement('label');
                label.textContent = pop.PopulationName;
                label.insertBefore(checkbox, label.firstChild);

                populationContainer.appendChild(label);
            });
        })
        .catch(error => console.error('Error fetching populations:', error));

    // Event listener for the analyze button
    document.getElementById('analyze-btn').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = {
            geneName: $('#gene-name').val(),
            superpopulations: [],
            populations: []
        };

        // Collect superpopulation checkbox values
        $('input[name="superpopulations"]:checked').each(function() {
            formData.superpopulations.push(this.value);
        });

        // Collect population checkbox values
        $('input[name="populations"]:checked').each(function() {
            formData.populations.push(this.value);
        });

        // AJAX request to analyze admixture
        fetch('/analyze_admixture', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(response => {
            console.log('Analysis Results:', response);
            // Here you should add the logic to display the results
            // For instance, updating a chart or a table with the new data
        })
        .catch(error => {
            console.error('Error:', error);
            // Display error message to the user
        });
    });
});
