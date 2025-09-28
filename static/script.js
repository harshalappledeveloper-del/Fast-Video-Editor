document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const statusDiv = document.getElementById('status');
    const resultDiv = document.getElementById('result');

    statusDiv.textContent = 'Uploading and processing... This may take a while.';
    resultDiv.innerHTML = '';

    try {
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            statusDiv.textContent = 'Processing complete!';
            const downloadLink = document.createElement('a');
            downloadLink.href = result.download_url;
            downloadLink.textContent = 'Download Combined Video';
            downloadLink.setAttribute('download', '');
            resultDiv.appendChild(downloadLink);
        } else {
            statusDiv.textContent = `Error: ${result.error || 'An unknown error occurred.'}`;
        }
    } catch (error) {
        statusDiv.textContent = 'An unexpected error occurred. Please check the console for details.';
        console.error('Error during fetch:', error);
    }
});