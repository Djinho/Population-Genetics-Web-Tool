$(document).ready(function() {
    var tableBody = $('#snpTableBody');
    var snpIdSearch = $('#snpIdSearch');
    var geneNameSearch = $('#geneNameSearch');
    var positionSearch = $('#positionSearch');

    function highlightMatchingRows() {
        var searchValueSnpId = snpIdSearch.val().toLowerCase().trim();
        var searchValueGeneName = geneNameSearch.val().toLowerCase().trim();
        var searchValuePosition = positionSearch.val().toLowerCase().trim();

        // Remove any previous highlight
        tableBody.find('tr').removeClass('selected-row');
        let firstMatchFound = false; // Flag to track if the first match has been found

        if (searchValueSnpId === '' && searchValueGeneName === '' && searchValuePosition === '') {
            return;
        }

        var rows = tableBody.find('tr');

        // Iterate over rows to find and highlight the exact match
        rows.each(function() {
            var row = $(this);
            var cellTextSnpId = row.find('td:nth-child(2)').text().toLowerCase().trim(); // SNP ID is in the second column
            var cellTextGeneName = row.find('td:nth-child(3)').text().toLowerCase().trim(); // Gene Name is in the third column
            var cellTextPosition = row.find('td:nth-child(1)').text().toLowerCase().trim(); // Position is in the first column

            // Highlight the row that exactly matches the search value
            if (cellTextSnpId === searchValueSnpId || cellTextGeneName === searchValueGeneName || cellTextPosition === searchValuePosition) {
                row.addClass('selected-row');
                if (!firstMatchFound) {
                    // Attempt to center the first matching row in the viewport
                    row[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstMatchFound = true; // Update flag to avoid scrolling to other matches
                }
            }
        });
    }

    $('.search-box').keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault(); // Prevent form submission on 'Enter' press
            highlightMatchingRows(); // Call function to highlight and scroll
        }
    });

    function updateSelectionCounter() {
        var selectedCount = $('.snp-checkbox:checked').length;
        $('#selection-counter').text('Selected SNPs: ' + selectedCount);
        // Alert user when 100 SNPs are selected
        if (selectedCount === 100) {
            alert('100 SNPs have been selected.');
        }
    }

    $('.snp-checkbox').change(updateSelectionCounter);

    function handleSelectDeselect() {
        $('#select-all-snps').click(function() {
            $('.snp-checkbox').prop('checked', true);
            updateSelectionCounter();
        });
        $('#deselect-all-snps').click(function() {
            $('.snp-checkbox').prop('checked', false);
            updateSelectionCounter();
        });
    }

    function handlePopulationSelectDeselect() {
        $('#select-all-pop').click(function() {
            $('.population-checkbox').prop('checked', true);
        });
        $('#deselect-all-pop').click(function() {
            $('.population-checkbox').prop('checked', false);
        });
    }

    $('input[type="submit"]').click(function(e) {
        e.preventDefault();
        $('input[name="action"]').remove();
        $('<input>').attr({type: 'hidden', name: 'action', value: $(this).val()}).appendTo($(this).closest('form'));
        $(this).closest('form').submit();
    });

    handleSelectDeselect();
    handlePopulationSelectDeselect();
});
