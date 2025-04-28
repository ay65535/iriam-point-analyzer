document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData();
    const file = document.getElementById('fileInput').files[0];
    if (file) {
        formData.append('file', file);
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('ocrResults').textContent = data.error;
            } else {
                document.getElementById('ocrResults').textContent = JSON.stringify(data.data, null, 2);
                document.getElementById('downloadLink').href = `/download/${data.csv}`;
            }
        })
        .catch(error => {
            document.getElementById('ocrResults').textContent = 'Error: ' + error;
        });
    }
});
