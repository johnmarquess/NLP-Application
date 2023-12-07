document.addEventListener('DOMContentLoaded', function () {
    function setupColumnSelector(fileSelectId, columnSelectId, allColumnsCheckId) {
        var fileSelect = document.getElementById(fileSelectId);
        var columnSelect = document.getElementById(columnSelectId);
        var allColumnsCheck = document.getElementById(allColumnsCheckId);
        var urlTemplate = document.getElementById('columns-url').getAttribute('data-url');

        // Function to update column select visibility
        function updateColumnSelectVisibility() {
            if (allColumnsCheck && allColumnsCheck.checked) {
                columnSelect.style.display = 'none';
            } else {
                columnSelect.style.display = 'block';
            }
        }

        // Setup event listener for file select
        if (fileSelect && columnSelect) {
            fileSelect.addEventListener('change', function () {
                var filename = this.value;
                if (filename) {
                    var url = urlTemplate + filename;
                    fetch(url)
                        .then(response => response.json())
                        .then(data => {
                            if (data.error) {
                                alert('Error: ' + data.error);
                            } else {
                                columnSelect.innerHTML = '';
                                data.forEach(function (column) {
                                    var option = new Option(column, column);
                                    columnSelect.add(option);
                                });

                                // Set 'processed_data' as selected if it exists
                                var processedDataOption = Array.from(columnSelect.options).find(opt => opt.value === 'processed_data');
                                if (processedDataOption) {
                                    columnSelect.value = 'processed_data';
                                }

                                // Update visibility based on the state of 'Select All Columns' checkbox
                                updateColumnSelectVisibility();
                            }
                        }).catch(error => console.error('Fetch Error:', error));
                }
            });
        }

        // Setup event listener for 'Select All Columns' checkbox
        if (allColumnsCheck) {
            allColumnsCheck.addEventListener('change', updateColumnSelectVisibility);
        }
    }

    // Setup for different contexts
    setupColumnSelector('data-processing-file-select', 'data-processing-column-select', 'data-processing-all-columns-check');
    setupColumnSelector('model-builder-file-select', 'model-builder-column-select', 'model-builder-all-columns-check');
});
