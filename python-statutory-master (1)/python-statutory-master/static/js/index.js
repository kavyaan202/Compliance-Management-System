// edit and delete functions
function openEditComplianceModal(id, complianceDetails, nameOfStatutory, frequency,DocumentReferenceNumber, validFrom, validUpto, remarks) {
    document.getElementById('editComplianceDetails').value = complianceDetails;
    document.getElementById('editNameOfStatutory').value = nameOfStatutory;
    document.getElementById('editFrequency').value = frequency;
    document.getElementById('editDocument_Reference_Number').value=DocumentReferenceNumber
    document.getElementById('editValidFrom').value = validFrom;
    document.getElementById('editValidUpto').value = validUpto;
    document.getElementById('editRemarks').value = remarks;

    // Set the form action using the compliance ID
    document.getElementById('editComplianceForm').action = "/edit_compliance/" + id;
}

document.getElementById('editComplianceForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    const formData = new FormData(this);
    const id = this.action.split("/").pop(); // Get the compliance ID from the action URL

    fetch(this.action, {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              // Update the row in the table
              const row = document.getElementById(`compliance-${id}`);
              row.cells[0].innerText = document.getElementById('editComplianceDetails').value;
              row.cells[1].innerText = document.getElementById('editNameOfStatutory').value;
              row.cells[2].innerText = document.getElementById('editFrequency').value;
              row.cells[3].innerText = document.getElementById('editDocument_Reference_Number').value;
              row.cells[4].innerText = document.getElementById('editValidFrom').value;
              row.cells[5].innerText = document.getElementById('editValidUpto').value;
              row.cells[6].innerText = document.getElementById('editRemarks').value;

              // Close the modal (if needed)
              $('#editComplianceModal').modal('hide');
          } else {
              // Handle errors
              alert('Failed to update compliance. Please try again.');
          }
      }).catch(error => console.error('Error:', error));
});
function prepareDelete(index) {
    debugger;
    // Set the form action for delete
    document.getElementById('deleteComplianceForm').action = "/delete_compliance/" + index;
}
function applyStatutoryFilter() {
    var statutoryFilter = document.getElementById('statutoryFilter').value;
    var currentUrl = new URL(window.location.href);

    // Update URL with filter parameter
    currentUrl.searchParams.set('statutory_filter', statutoryFilter);
    
    // Reset the page to 1 when a new filter is applied
    currentUrl.searchParams.set('page', 1);

    window.location.href = currentUrl.toString();
}

document.addEventListener('DOMContentLoaded', function() {
    const statutoryFilter = document.getElementById('statutoryFilter');

    // Apply filter when statutory filter is changed
    statutoryFilter.addEventListener('change', applyStatutoryFilter);

    // Set initial value from URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    statutoryFilter.value = urlParams.get('statutory_filter') || '';
});
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener for the search input
    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener('input', performSearch);
    }
});

function performSearch() {
    // Get the search input
    var input = document.getElementById("searchInput");
    var filter = input.value.toUpperCase();
    var table = document.getElementById("complianceTable");
    var tr = table.getElementsByTagName("tr");

    // Loop through all table rows, starting from index 1 to skip the header
    for (var i = 1; i < tr.length; i++) {
        var found = false;
        var td = tr[i].getElementsByTagName("td");
        for (var j = 0; j < td.length; j++) {
            var cell = td[j];
            if (cell) {
                var textValue = cell.textContent || cell.innerText;
                if (textValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        if (found) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}

// Expose functions to the global scope if needed (optional)
window.openEditComplianceModal = openEditComplianceModal;
window.prepareDelete = prepareDelete;
window.performSearch = performSearch;
// document.addEventListener('DOMContentLoaded', function() {
//     const statutoryFilter = document.getElementById('statutoryFilter');
//     const complianceTable = document.querySelector('.table-striped tbody');

//     statutoryFilter.addEventListener('change', function() {
//         const selectedStatutory = this.value;
//         const rows = complianceTable.querySelectorAll('tr');

//         rows.forEach(row => {
//             const statutoryCell = row.querySelector('td:nth-child(2)'); // Assuming Name of Statutory is the second column
//             if (selectedStatutory === '' || statutoryCell.textContent === selectedStatutory) {
//                 row.style.display = '';
//             } else {
//                 row.style.display = 'none';
//             }
//         });
//     });
// });

// function performSearch() {
//     // Get the search input
//     var input = document.getElementById("searchInput");
//     var filter = input.value.toUpperCase();
//     var table = document.getElementById("complianceTable");
//     var tr = table.getElementsByTagName("tr");

//     // Loop through all table rows, starting from index 1 to skip the header
//     for (var i = 1; i < tr.length; i++) {
//         var found = false;
//         var td = tr[i].getElementsByTagName("td");
//         for (var j = 0; j < td.length; j++) {
//             var cell = td[j];
//             if (cell) {
//                 var textValue = cell.textContent || cell.innerText;
//                 if (textValue.toUpperCase().indexOf(filter) > -1) {
//                     found = true;
//                     break;
//                 }
//             }
//         }
//         if (found) {
//             tr[i].style.display = "";
//         } else {
//             tr[i].style.display = "none";
//         }
//     }
// }

// // Expose functions to the global scope if needed (optional)
// window.openEditComplianceModal = openEditComplianceModal;
// window.prepareDelete = prepareDelete;
// window.performSearch = performSearch;



// // search and filter function
// function performSearch() {
//     var searchQuery = document.getElementById('searchInput').value;
//     var statutoryFilter = document.getElementById('statutoryFilter').value;
//     var currentUrl = new URL(window.location.href);

//     // Update URL with search and filter parameters
//     currentUrl.searchParams.set('search', searchQuery);
//     currentUrl.searchParams.set('statutory_filter', statutoryFilter);
    
//     // Reset the page to 1 when a new search or filter is applied
//     currentUrl.searchParams.set('page', 1);

//     window.location.href = currentUrl.toString();
// }


// document.addEventListener('DOMContentLoaded', function() {
//     const searchInput = document.getElementById('searchInput');
//     const statutoryFilter = document.getElementById('statutoryFilter');
//     const searchButton = document.getElementById('searchButton');

//     // Perform search when the search button is clicked
//     searchButton.addEventListener('click', performSearch);

//     // Perform search when Enter key is pressed in the search input
//     searchInput.addEventListener('keypress', function(e) {
//         if (e.key === 'Enter') {
//             performSearch();
//         }
//     });


//     // Perform search when statutory filter is changed
//     statutoryFilter.addEventListener('change', performSearch);

//     // Set initial values from URL parameters
//     const urlParams = new URLSearchParams(window.location.search);
//     searchInput.value = urlParams.get('search') || '';
//     statutoryFilter.value = urlParams.get('statutory_filter') || '';
// });
