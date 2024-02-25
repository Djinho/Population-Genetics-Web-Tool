$(document).ready(function() {
    function debounce(func, wait) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                func.apply(context, args);
            }, wait);
        };
    }

    function initializeTableFiltering() {
        var positionSearch = $('#positionSearch');
        var snpIdSearch = $('#snpIdSearch');
        var geneNameSearch = $('#geneNameSearch');
        var tableBody = $('#snpTableBody');

        function filterTableAndScroll() {
            var positionValue = positionSearch.val().toLowerCase();
            var snpIdValue = snpIdSearch.val().toLowerCase();
            var geneNameValue = geneNameSearch.val().toLowerCase();
            
            // Temporarily detach table body for efficient manipulation
            var detachedBody = tableBody.detach();
            var rows = detachedBody.find('tr').toArray();
            var foundRow = null;

            rows.forEach(function(row) {
                var $row = $(row);
                var rowText = $row.text().toLowerCase();
                var match = rowText.includes(positionValue) && rowText.includes(snpIdValue) && rowText.includes(geneNameValue);
                if (match && !foundRow) {
                    foundRow = $row;
                }
                $row.toggle(match);
            });

            // Reattach the table body
            $('#snpTableBody').replaceWith(detachedBody);

            if (foundRow) {
                $('.scrollTable').animate({
                    scrollTop: foundRow.position().top + $('.scrollTable').scrollTop() - $('.scrollTable').position().top
                }, 500);
            } else {
                $('.scrollTable').scrollTop(0);
            }
        }

        var debouncedFilter = debounce(filterTableAndScroll, 250);
        positionSearch.on('input', debouncedFilter);
        snpIdSearch.on('input', debouncedFilter);
        geneNameSearch.on('input', debouncedFilter);
    }

    // Retaining the existing form submission handling and select/deselect functionalities
    function handleSelectDeselect() {
        $('#select-all-pop').click(function() { $('.population-checkbox').prop('checked', true); });
        $('#deselect-all-pop').click(function() { $('.population-checkbox').prop('checked', false); });
        $('#select-all-snps').click(function() { $('.snp-checkbox').prop('checked', true); });
        $('#deselect-all-snps').click(function() { $('.snp-checkbox').prop('checked', false); });
    }

    $('input[type="submit"]').click(function(e) {
        e.preventDefault();
        $('input[name="action"]').remove();
        $('<input>').attr({ type: 'hidden', name: 'action', value: $(this).val() }).appendTo($(this).closest('form'));
        $(this).closest('form').submit();
    });

    // Initialize functionalities
    initializeTableFiltering();
    handleSelectDeselect();
});
