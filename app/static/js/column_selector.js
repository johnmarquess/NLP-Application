document.addEventListener('DOMContentLoaded', function () {
    function setupColumnSelector(fileSelectId, columnSelectId) {
        var fileSelect = document.getElementById(fileSelectId);
        var columnSelect = document.getElementById(columnSelectId);
        var urlTemplate = document.getElementById('columns-url').getAttribute('data-url');

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
                            }
                        }).catch(error => console.error('Fetch Error:', error));
                }
            });
        }
    }

    // Setup for different contexts
    setupColumnSelector('data-processing-file-select', 'data-processing-column-select');
    setupColumnSelector('model-builder-file-select', 'model-builder-column-select');
});
