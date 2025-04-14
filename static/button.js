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
    
    // Open camera when attachment button is clicked
    attachBtn.addEventListener('click', function () {
      cameraContainer.style.display = 'block';  // Show camera container
      startCamera();
    });
    
    // Start the camera stream
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
    
    // Capture image when capture button is clicked
    captureBtn.addEventListener('click', function () {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
      // Convert image to base64 string
      const imageData = canvas.toDataURL('image/png');
    
      // Send the image to the backend
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
    
      // Hide camera after capture
      cameraContainer.style.display = 'none';
    });
    
    // Handle sending text messages
    sendBtn.addEventListener('click', function () {
        const userMessage = textInput.value.trim();
        if (userMessage === '') return;
      
        const outgoingMsg = document.createElement('li');
        outgoingMsg.className = 'chat outgoing';
        outgoingMsg.innerHTML = `<p>${userMessage}</p>`;
        chatBox.appendChild(outgoingMsg);
        textInput.value = '';
      
        // Send the user message to Groq for a response
        fetch('/groq-response', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
          const botMsg = document.createElement('li');
          botMsg.className = 'chat incoming';
          botMsg.innerHTML = `<span class="material-symbols-outlined">heart_plus</span>
                              <p>${data.reply}</p>`;  // Groq reply goes here
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
    
    // Settings dropdown toggle
    const settingsBtn = document.getElementById('settings-btn');
    const settingsDropdown = document.getElementById('settings-dropdown');
    
    // Toggle the settings dropdown
    settingsBtn.addEventListener('click', function () {
      settingsDropdown.classList.toggle('show');
    });
  });
  