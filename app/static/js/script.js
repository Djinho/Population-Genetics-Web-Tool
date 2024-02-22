$(document).ready(function() {
    // Column-specific search functionalities
    $('#positionSearch').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $("table tbody tr").filter(function() {
            $(this).toggle($(this).find('td:eq(0)').text().toLowerCase().indexOf(value) > -1)
        });
    });

    $('#snpIdSearch').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $("table tbody tr").filter(function() {
            $(this).toggle($(this).find('td:eq(1)').text().toLowerCase().indexOf(value) > -1)
        });
    });

    $('#geneNameSearch').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $("table tbody tr").filter(function() {
            $(this).toggle($(this).find('td:eq(2)').text().toLowerCase().indexOf(value) > -1)
        });
    });

    // Handling checkbox selection for SNPs
    $('table tbody').on('change', 'input[type="checkbox"]', function() {
        var selectedSnps = [];
        $('table tbody input[type="checkbox"]:checked').each(function() {
            selectedSnps.push($(this).closest('tr').data('snp-id'));
        });
        $('#selectedSnps').val(selectedSnps.join(','));
    });

    // Existing code for fetching populations
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

    // Handling the analysis button click event
    document.getElementById('analyze-btn').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = {
            geneName: $('#gene-name').val(),
            superpopulations: [],
            populations: [],
            selectedSnps: $('#selectedSnps').val().split(',')
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
            // Here, add logic to display the results, such as updating a chart or table
        })
        .catch(error => {
            console.error('Error:', error);
            // Display error message to the user
        });
    });
});
