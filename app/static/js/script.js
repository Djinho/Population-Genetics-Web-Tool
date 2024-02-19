document.addEventListener('DOMContentLoaded', function() {
    // Fetch populations and populate checkboxes
    fetch('/get_populations')
        .then(response => response.json())
        .then(data => {
            const superPopulationContainer = document.querySelector('.superpopulation-checkbox-group');
            const populationContainer = document.querySelector('.population-checkbox-group');

            // Assuming data is an object with 'superpopulations' and 'populations' arrays
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

    // Add event listener to the analyze button
    document.getElementById('analyze-btn').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default form submission

        // Prepare formData object
        var formData = {
            superpopulations: [],
            populations: []
        };

        // Collect superpopulation checkbox values
        document.querySelectorAll('input[name="superpopulations"]:checked').forEach((checkbox) => {
            formData.superpopulations.push(checkbox.value);
        });

        // Collect population checkbox values
        document.querySelectorAll('input[name="populations"]:checked').forEach((checkbox) => {
            formData.populations.push(checkbox.value);
        });

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
            // Pass data to interactive_plot.js for chart rendering or handle it here as needed
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error, e.g., display error message to user
        });
    });
});
