document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyze-button');
    const heatmapButton = document.getElementById('heatmap-button');
    
    // Function to generate the stacked bar chart
    function generateAdmixturePlot(selectedPopulations) {
        fetch('/analyze_admixture', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ populations: selectedPopulations }),
        })
        .then(response => response.json())
        .then(plot_data => {
            var colors = [
                'rgba(255, 0, 0, 1)', // Red for Ancestry 1
                'rgba(0, 0, 255, 1)', // Blue for Ancestry 2
                'rgba(0, 128, 0, 1)', // Green for Ancestry 3
                'rgba(128, 0, 128, 1)', // Purple for Ancestry 4
                'rgba(255, 255, 0, 1)' // Yellow for Ancestry 5
            ];

            plot_data.forEach((trace, index) => {
                trace.marker = { color: colors[index % colors.length] };
            });

            var layout = {
                barmode: 'stack',
                title: 'Admixture Analysis',
                xaxis: { title: 'Population' },
                yaxis: { title: 'Ancestry Proportion' }
            };

            Plotly.newPlot('admixturePlot', plot_data, layout);
            heatmapButton.style.display = 'block'; // Show the heatmap button after plotting
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    // Event listener for the analyze button
    if (analyzeButton) {
        analyzeButton.addEventListener('click', function() {
            const selectedPopulations = Array.from(document.querySelectorAll('input[name="populations[]"]:checked')).map(checkbox => checkbox.value);
            generateAdmixturePlot(selectedPopulations);
        });
    }
    
    // Function to generate the heatmap
    function generateHeatmap(selectedPopulations) {
        fetch('/admixture_heatmap', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ populations: selectedPopulations }),
        })
        .then(response => response.json())
        .then(heatmap_data => {
            var data = [{
                z: heatmap_data.values,
                x: heatmap_data.x_labels, // populations
                y: heatmap_data.y_labels, // ancestries
                type: 'heatmap',
                colorscale: 'Viridis',
            }];

            var layout = {
                title: 'Admixture Heatmap',
                xaxis: { title: 'Population' },
                yaxis: { title: 'Ancestry' }
            };

            Plotly.newPlot('admixturePlot', data, layout);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Function to handle downloading the heatmap
    function downloadHeatmap(selectedPopulations) {
        fetch('/download_heatmap', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ populations: selectedPopulations }),
        })
        .then(response => response.blob())
        .then(blob => {
            // Create a new link element
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'admixture_heatmap.png';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));
    }

    // Event listener for the heatmap download button
    if (heatmapButton) {
        heatmapButton.addEventListener('click', function() {
            const selectedPopulations = Array.from(document.querySelectorAll('input[name="populations[]"]:checked')).map(checkbox => checkbox.value);
            downloadHeatmap(selectedPopulations);
        });
    }
});
