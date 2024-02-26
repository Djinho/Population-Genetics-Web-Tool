$(document).ready(function() {
    $('.search-box').on('input', function() { // Respond immediately to input changes
        searchAndScroll();
    });

    function searchAndScroll() {
        var positionValue = $('#positionSearch').val().toLowerCase();
        var snpIdValue = $('#snpIdSearch').val().toLowerCase();
        var geneNameValue = $('#geneNameSearch').val().toLowerCase();

        var found = false; // Flag to identify if any matching row is found
        
        $('#snpTableBody tr').css('background-color', ''); // Reset any previous highlighting

        if (!positionValue && !snpIdValue && !geneNameValue) {
            // If all search fields are empty, avoid unnecessary processing
            return;
        }

        $('#snpTableBody tr').each(function() {
            var $this = $(this);
            // Extract text for each specified field
            var positionText = $this.find('td:nth-child(1)').text().toLowerCase();
            var snpIdText = $this.find('td:nth-child(2)').text().toLowerCase();
            var geneNameText = $this.find('td:nth-child(3)').text().toLowerCase();

            // Check if the row matches all non-empty search fields
            if (positionText.includes(positionValue) && snpIdText.includes(snpIdValue) && geneNameText.includes(geneNameValue) && !found) {
                $('html, body').animate({
                    scrollTop: $this.offset().top - $('.scrollTable').offset().top + $('.scrollTable').scrollTop()
                }, 500);
                $this.css('background-color', '#add8e6'); // Highlight the first matching row
                found = true; // Avoid scrolling to other rows and multiple highlights
            }
        });

        if (!found) { // Optionally handle case where no rows are found
            console.log("No matches found!"); // Placeholder action, e.g., showing a message
        }
    }

    // Implementation for preventing form submission on 'Enter' press
    $('.search-box').keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
        }
    });

    // Below this point, append your existing code for selection counters and checkbox handlers
});

    // Update selection counter
    function updateSelectionCounter() {
        var selectedCount = $('.snp-checkbox:checked').length;
        $('#selection-counter').text('Selected SNPs: ' + selectedCount);
    }
    
    // Attach event handlers for checkboxes to update the selection counter
    $('.snp-checkbox').change(updateSelectionCounter);

    // Handlers for 'Select All' and 'Deselect All' actions
    $('#select-all-snps').click(function() {
        $('.snp-checkbox').prop('checked', true);
        updateSelectionCounter();
    });
    
    $('#deselect-all-snps').click(function() {
        $('.snp-checkbox').prop('checked', false);
        updateSelectionCounter();
    });
});
