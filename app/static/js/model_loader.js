const modelSelect = document.getElementById('model-select');
modelSelect.addEventListener('change', function () {
    const selectedModel = this.value;
    fetch('/load-model', {
        method: 'POST', headers: {
            'Content-Type': 'application/json', 'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
        }, body: JSON.stringify({model: selectedModel})
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            // Handle success or error messages from server
            if (data.status === 'success') {
                // Model loaded successfully
            } else {
                // Handle error
            }
        });
});

