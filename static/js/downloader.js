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
    const isMp4 = selected === 'mp4';

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

const setupTabs = () => {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            tabButtons.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            const panel = document.getElementById(targetId);
            if (panel) panel.classList.add('active');
        });
    });
};

const setupFfmpegVerify = () => {
    const verifyBtn = document.getElementById('ffmpeg-verify-btn');
    const statusPill = document.getElementById('ffmpeg-status');
    if (!verifyBtn || !statusPill) return;

    verifyBtn.addEventListener('click', async () => {
        statusPill.textContent = 'Checking...';
        statusPill.className = 'status-pill neutral';

        try {
            const resp = await fetch('/api/verify-ffmpeg', { method: 'GET' });
            const data = await resp.json();

            if (data.ok) {
                statusPill.textContent = 'Verified';
                statusPill.className = 'status-pill ok';
            } else {
                statusPill.textContent = 'Not found';
                statusPill.className = 'status-pill bad';
            }
        } catch (e) {
            statusPill.textContent = 'Error';
            statusPill.className = 'status-pill bad';
        }
    });
};

document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    setupFfmpegVerify();
    toggleOptions();

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

    const selectedFormat = document.querySelector('input[name="format"]:checked')?.value || 'mp3';
    const resolution = document.getElementById('resolution')?.value || '720';
    const bitrate = document.getElementById('bitrate')?.value || 'best';

    const useCustomDir = document.getElementById('use-custom-dir').checked;
    const customDirectory = useCustomDir ? document.getElementById('custom-directory').value.trim() : '';

    btn.disabled = true;
    message.innerHTML = '';

    if (useCustomDir && customDirectory && customDirectory.length < 3) {
        showError('Please enter a valid directory path');
        btn.disabled = false;
        return;
    }

    const formData = new URLSearchParams({
        url: url,
        format: selectedFormat,
        resolution: resolution,
        bitrate: bitrate,
        ...(useCustomDir && customDirectory && { custom_directory: customDirectory })
    });

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

document.getElementById("history-btn").addEventListener("click", () => {
    fetch("/history")
        .then(response => response.json())
        .then(data => {
            const box = document.getElementById("history-box")
            if (data.history.length === 0) {
                box.textContent = "No downloads yet"
            } else {
                let tableHTML = `
                    <table>
                        <thead>
                            <tr>
                                <th>Title</th>
                            </tr>
                        </thead>
                        <tbody>
                `;
                
                data.history.forEach(entry => {
                    tableHTML += `
                        <tr>
                            <td>${entry}</td>
                        </tr>
                    `;
                });
                
                tableHTML += `
                        </tbody>
                    </table>
                `;
                
                box.innerHTML = tableHTML;
            }
            
            box.style.display = "block";
        });
});

