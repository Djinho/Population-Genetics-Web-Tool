function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function initializeTableFiltering() {
    const positionSearch = $('#positionSearch');
    const snpIdSearch = $('#snpIdSearch');
    const geneNameSearch = $('#geneNameSearch');
    const snpTableBody = $('#snpTableBody');

    function filterTable() {
        const positionValue = positionSearch.val().toLowerCase();
        const snpIdValue = snpIdSearch.val().toLowerCase();
        const geneNameValue = geneNameSearch.val().toLowerCase();

        snpTableBody.find('tr').filter(function() {
            $(this).toggle(
                $(this).text().toLowerCase().indexOf(positionValue) > -1 &&
                $(this).text().toLowerCase().indexOf(snpIdValue) > -1 &&
                $(this).text().toLowerCase().indexOf(geneNameValue) > -1
            );
        });
    }

    // Debouncing filter function
    positionSearch.on('keyup', debounce(filterTable, 250));
    snpIdSearch.on('keyup', debounce(filterTable, 250));
    geneNameSearch.on('keyup', debounce(filterTable, 250));
}



document.addEventListener('DOMContentLoaded', (event) => {
    let maxGenes = 100;
    const counterDisplay = document.getElementById('maxCounter');
  
    // Function to update the counter
    function updateCounter() {
      const selectedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked').length;
      console.log('Selected Checkboxes:', selectedCheckboxes); // Debugging line
      counterDisplay.textContent = maxGenes - selectedCheckboxes;
    }
  
    // Add change event listener to all checkboxes
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    console.log('Total Checkboxes:', checkboxes.length); // Debugging line
  
    checkboxes.forEach((checkbox, index) => {
      checkbox.addEventListener('change', () => {
        console.log('Checkbox ' + index + ' changed'); // Debugging line
        if(document.querySelectorAll('input[type="checkbox"]:checked').length > maxGenes) {
          alert('Maximum limit reached');
          checkbox.checked = false;
        }
        updateCounter();
      });
    });
  
    // Initialize the counter for the first time
    updateCounter();
  });
  
  

  
// This function captures the selected SNP IDs and submits them with the form
function captureAndSubmitSelectedSNPs() {
    $('form').submit(function(e) {
        // Prevent the default form submission to manually handle the data
        e.preventDefault();

        // Capture selected SNP IDs
        var selectedSnps = $('input[type="checkbox"][name="selected_snps[]"]:checked')
                            .map(function() { return this.value; }).get();
        
        // Optional: Log the selected SNPs for debugging
        console.log("Selected SNPs:", selectedSnps);

        // Append selected SNP IDs to a hidden input field or directly submit the form here
        // For example, you might adjust the form data here if needed before submission

        // Submit the form
        // e.currentTarget.submit(); // Uncomment this if you need to manually submit after processing

        // If you're using AJAX to submit the form, construct your AJAX request here
        // and include 'selectedSnps' with the data you're sending to the server
    });
}

$(document).ready(function() {
    initializeTableFiltering();
    // Initialize the function to capture and submit selected SNPs
    captureAndSubmitSelectedSNPs();
});
