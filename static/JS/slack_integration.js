function openSlackModal(message) {
    document.getElementById('slackMessage').value = message;
    new bootstrap.Modal(document.getElementById('slackModal')).show();
}

document.getElementById('slackRecipient').addEventListener('input', async function() {
    const query = this.value;
    const resultsDiv = document.getElementById('slackResults');
    resultsDiv.innerHTML = '';

    if (query.length > 2) {
        try {
            const response = await fetch(`/search_slack?query=${query}`);
            const results = await response.json();

            if (results.success) {
                results.data.forEach(item => {
                    const div = document.createElement('div');
                    div.classList.add('form-check');
                    
                    const input = document.createElement('input');
                    input.classList.add('form-check-input');
                    input.type = 'checkbox';
                    input.value = item.id;
                    input.id = `slack-${item.id}`;
                    
                    const label = document.createElement('label');
                    label.classList.add('form-check-label');
                    label.htmlFor = `slack-${item.id}`;
                    label.textContent = item.name;
                    
                    div.appendChild(input);
                    div.appendChild(label);
                    resultsDiv.appendChild(div);
                });
            }
        } catch (error) {
            console.error('Error fetching Slack search results:', error);
        }
    }
});

async function sendMessageToSlack() {
    const selectedRecipients = Array.from(document.querySelectorAll('#slackResults .form-check-input:checked')).map(input => input.value);
    const message = document.getElementById('slackMessage').value;

    try {
        const response = await fetch('/send_to_slack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ recipients: selectedRecipients, message })
        });
        const result = await response.json();
        if (result.success) {
            alert('Message sent to Slack successfully');
            new bootstrap.Modal(document.getElementById('slackModal')).hide();
        } else {
            alert('Error sending message to Slack: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
