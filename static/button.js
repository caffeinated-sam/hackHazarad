document.addEventListener('DOMContentLoaded', function () {
  const attachBtn = document.getElementById('attachment');
  const cameraContainer = document.getElementById('camera-container');
  const video = document.getElementById('video');
  const captureBtn = document.getElementById('capture');
  const canvas = document.getElementById('canvas');
  const context = canvas.getContext('2d');
  const chatBox = document.querySelector('.chatbox');
  const sendBtn = document.querySelector('.chat-input span.material-symbols-outlined:last-of-type');
  const textInput = document.querySelector('.chat-input textarea');
  const closeCameraBtn = document.getElementById('close-camera');

  // Open camera
  attachBtn.addEventListener('click', function () {
    cameraContainer.style.display = 'block';
    startCamera();
  });

  function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function (stream) {
        video.srcObject = stream;
      })
      .catch(function (error) {
        console.log('Error accessing the camera: ', error);
        alert('Could not access camera');
      });
  }

  // Close camera
  closeCameraBtn.addEventListener('click', function () {
    const stream = video.srcObject;
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      video.srcObject = null;
    }
    cameraContainer.style.display = 'none';
  });

  // Capture image
  captureBtn.addEventListener('click', function () {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');

    fetch('/upload-image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ image: imageData }),
    })
    .then(response => response.json())
    .then(data => {
      const botMsg = document.createElement('li');
      botMsg.className = 'chat incoming';
      botMsg.innerHTML = `<span class="material-symbols-outlined">photo_camera</span>
                          <p>Image received! 🖼️</p>`;
      chatBox.appendChild(botMsg);
      chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
      console.log('Error sending image:', error);
      alert('Something went wrong while uploading the image.');
    });

    cameraContainer.style.display = 'none';
  });

  // Send message
  sendBtn.addEventListener('click', function () {
    const userMessage = textInput.value.trim();
    if (userMessage === '') return;

    const outgoingMsg = document.createElement('li');
    outgoingMsg.className = 'chat outgoing';
    outgoingMsg.innerHTML = `<p>${userMessage}</p>`;
    chatBox.appendChild(outgoingMsg);
    textInput.value = '';

    fetch('/groq-response', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: userMessage }),  // 👈 this should match what your Flask route expects
    })    
    .then(response => response.json())
    .then(data => {
      const botMsg = document.createElement('li');
      botMsg.className = 'chat incoming';
      botMsg.innerHTML = `<span class="material-symbols-outlined">heart_plus</span>
                          <p>${data.reply}</p>`;
      chatBox.appendChild(botMsg);
      chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
      console.log('Error receiving Groq response:', error);
      const botMsg = document.createElement('li');
      botMsg.className = 'chat incoming';
      botMsg.innerHTML = `<span class="material-symbols-outlined">error</span>
                          <p>Oops! Something went wrong. Please try again later.</p>`;
      chatBox.appendChild(botMsg);
      chatBox.scrollTop = chatBox.scrollHeight;
    });
  });

  // Enable "Enter" to send
  textInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendBtn.click();
    }
  });

  // Toggle settings dropdown
  const settingsBtn = document.getElementById('settings-btn');
  const settingsDropdown = document.getElementById('settings-dropdown');
  settingsBtn.addEventListener('click', function () {
    settingsDropdown.classList.toggle('show');
  });
});
