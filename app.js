function showSessionForm() {
    document.getElementById('sessionForm').style.display = 'block';
}

async function sendCode() {
    const apiId = document.getElementById('apiId').value;
    const apiHash = document.getElementById('apiHash').value;
    const phone = document.getElementById('phone').value;
    
    const response = await fetch('http://localhost:5000/api/send_code', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({api_id: apiId, api_hash: apiHash, phone: phone})
    });
    
    const result = await response.json();
    if (!result.error) {
        document.getElementById('code').style.display = 'block';
        document.querySelector('#sessionForm button:nth-of-type(2)').style.display = 'block';
    }
}

async function confirmCode() {
    const code = document.getElementById('code').value;
    const apiId = document.getElementById('apiId').value;
    const apiHash = document.getElementById('apiHash').value;
    const phone = document.getElementById('phone').value;
    
    const response = await fetch('http://localhost:5000/api/confirm_code', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            api_id: apiId,
            api_hash: apiHash,
            phone: phone,
            code: code
        })
    });
    
    const result = await response.json();
    if (!result.error) {
        alert('Авторизация успешна!');
        document.getElementById('sessionForm').style.display = 'none';
    }
}