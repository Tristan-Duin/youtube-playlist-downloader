const form = document.getElementById('form');
const btn = document.getElementById('download-btn');
const message = document.getElementById('message');
const status = document.getElementById('status');
let interval;

const toggleOptions = () => {
    const selected = document.querySelector('input[name="format"]:checked')?.value;
    const resolutionBox = document.getElementById('resolution-box');
    const bitrateBox = document.getElementById('bitrate-box');
    
    const isMp3 = selected === 'mp3';
    const isMp4 = selected === 'mp4' || selected === 'mp4_playlist';
    
    if (resolutionBox) resolutionBox.style.display = isMp4 ? 'flex' : 'none';
    if (bitrateBox) bitrateBox.style.display = isMp3 ? 'flex' : 'none';
};

const toggleCustomDirectory = () => {
    const checkbox = document.getElementById('use-custom-dir');
    const inputDiv = document.getElementById('custom-dir-input');
    const textInput = document.getElementById('custom-directory');
    
    if (checkbox?.checked) {
        inputDiv.style.display = 'block';
        textInput.focus();
    } else {
        inputDiv.style.display = 'none';
        textInput.value = '';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    toggleOptions();
    
    // Event listeners for format toggles and custom directory
    document.querySelectorAll('input[name="format"]').forEach(radio => {
        radio.addEventListener('change', toggleOptions);
    });
    
    const customDirToggle = document.getElementById('use-custom-dir');
    if (customDirToggle) {
        customDirToggle.addEventListener('change', toggleCustomDirectory);
    }
});

const handleFormSubmit = async (e) => {
    e.preventDefault();
    
    const url = document.getElementById('url-input').value;
    // Check if custom directory feature is enabled
    const useCustomDir = document.getElementById('use-custom-dir').checked;
    const customDirectory = useCustomDir ? document.getElementById('custom-directory').value.trim() : '';
    
    btn.disabled = true;
    message.innerHTML = '';
    
    if (useCustomDir && customDirectory && customDirectory.length < 3) {
        showError('Please enter a valid directory path');
        btn.disabled = false;
        return;
    }

    // Include custom_directory in form data only if specified
    const formData = new URLSearchParams({ url: url, ...(useCustomDir && customDirectory && { custom_directory: customDirectory }) });
    
    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess('Download started!');
            startPolling();
        } else {
            showError(data.error || 'An error occurred');
            btn.disabled = false;
        }
    } catch (error) {
        showError(`Network error: ${error.message}`);
        btn.disabled = false;
    }
};

const showError = (msg) => {
    message.innerHTML = `<span class="error">${msg}</span>`;
};

const showSuccess = (msg) => {
    message.innerHTML = `<span class="success">${msg}</span>`;
};

form.addEventListener('submit', handleFormSubmit);

const startPolling = () => {
    interval = setInterval(async () => {
        try {
            const response = await fetch('/status');
            const data = await response.json();
            
            status.textContent = data.messages.join('\n');
            
            if (!data.in_progress) {
                btn.disabled = false;
                clearInterval(interval);
            }
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 1000);
};
