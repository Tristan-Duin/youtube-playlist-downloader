const form = document.getElementById('form');
const btn = document.getElementById('download-btn');
const message = document.getElementById('message');
const status = document.getElementById('status');
let interval;

form.onsubmit = async function(e) {
    e.preventDefault();
    const url = document.getElementById('url-input').value;
    
    btn.disabled = true;
    message.innerHTML = '';
    
    try {
        const res = await fetch('/download', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: 'url=' + encodeURIComponent(url)
        });
        
        const data = await res.json();
        
        if (res.ok) {
            message.innerHTML = '<span class="success">Download started!</span>';
            startPolling();
        } else {
            message.innerHTML = '<span class="error">' + data.error + '</span>';
            btn.disabled = false;
        }
    } catch (error) {
        message.innerHTML = '<span class="error">Error: ' + error.message + '</span>';
        btn.disabled = false;
    }
};

function startPolling() {
    interval = setInterval(async () => {
        const res = await fetch('/status');
        const data = await res.json();
        
        status.textContent = data.messages.join('\n');
        
        if (!data.in_progress) {
            btn.disabled = false;
            clearInterval(interval);
        }
    }, 1000);
}
