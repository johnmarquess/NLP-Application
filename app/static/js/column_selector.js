document.addEventListener('DOMContentLoaded', function () {
    var fileSelect = document.getElementById('file-select');
    var columnSelect = document.getElementById('column-select');
    var urlTemplate = document.getElementById('columns-url').getAttribute('data-url');

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
});

