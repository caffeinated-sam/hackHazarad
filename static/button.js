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
  const settingsBtn = document.getElementById('settings-btn');
  const settingsDropdown = document.getElementById('settings-dropdown');

  // Open camera when attachment button is clicked
  attachBtn.addEventListener('click', function () {
    cameraContainer.style.display = 'block';
    startCamera();
  });

  // Start video stream
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

  // Close camera when the user clicks the close button
  closeCameraBtn.addEventListener('click', function () {
    const stream = video.srcObject;
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      video.srcObject = null;
    }
    cameraContainer.style.display = 'none';
  });

  // Capture image and send it to the server
  captureBtn.addEventListener('click', function () {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');

    // Send captured image to the backend
    fetch('/upload-image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ image: imageData }),
    })
    .then(response => response.json())
    .then(data => {
      displayBotMessage('Image received! 🖼️', 'photo_camera');
    })
    .catch(error => {
      console.log('Error sending image:', error);
      alert('Something went wrong while uploading the image.');
    });

    cameraContainer.style.display = 'none';
  });

  // Send user message and get Groq response
  sendBtn.addEventListener('click', function () {
    const userMessage = textInput.value.trim();
    if (userMessage === '') return;

    displayUserMessage(userMessage);

    fetch('/groq-response', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: userMessage }),
    })    
    .then(response => response.json())
    .then(data => {
      displayBotMessage(data.reply, 'heart_plus');
    })
    .catch(error => {
      console.log('Error receiving Groq response:', error);
      displayBotMessage('Oops! Something went wrong. Please try again later.', 'error');
    });

    // Clear input and reset the textarea height
    textInput.value = '';
    resetTextarea();
  });

  // Function to reset the height of the textarea
  function resetTextarea() {
    textInput.style.height = 'auto'; // Reset height to auto
    textInput.style.height = (textInput.scrollHeight) + 'px'; // Set height based on content
  }

  // Adjust the height of the textarea as the user types
  textInput.addEventListener('input', function () {
    textInput.style.height = 'auto'; // Reset height before adjusting
    textInput.style.height = (textInput.scrollHeight) + 'px'; // Adjust height to match content
  });

  // Display user's message
  function displayUserMessage(message) {
    const outgoingMsg = document.createElement('li');
    outgoingMsg.className = 'chat outgoing';

    const p = document.createElement('p');
    p.style.whiteSpace = 'pre-wrap';  // Preserve spaces and line breaks
    p.textContent = message;         // Add the user's message
    outgoingMsg.appendChild(p);
    chatBox.appendChild(outgoingMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Display bot's message with typing animation
  function displayBotMessage(message, icon) {
    const botMsg = document.createElement('li');
    botMsg.className = 'chat incoming';

    const span = document.createElement('span');
    span.className = 'material-symbols-outlined';
    span.innerText = icon;

    const p = document.createElement('p');
    botMsg.appendChild(span);
    botMsg.appendChild(p);
    chatBox.appendChild(botMsg);

    let index = 0;
    const typingSpeed = 30;

    function typeChar() {
      if (index < message.length) {
        p.innerHTML += message[index] === '\n' ? '<br>' : message[index];
        index++;
        setTimeout(typeChar, typingSpeed);
      } else {
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    }

    p.innerHTML = '<span class="typing-dots">...</span>';
    setTimeout(() => {
      p.innerHTML = '';
      typeChar();
    }, 300); // Delay before typing starts
  }

  // Enable sending on "Enter" key press
  textInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendBtn.click();
    }
  });

  // Settings dropdown toggle
  settingsBtn.addEventListener('click', function () {
    settingsDropdown.classList.toggle('show');
  });

  // Close dropdown when clicking outside
  window.addEventListener('click', function (event) {
    if (!settingsBtn.contains(event.target) && !settingsDropdown.contains(event.target)) {
      settingsDropdown.classList.remove('show');
    }
  });

  // Optional: Submit question via form (if used somewhere else)
  const questionForm = document.querySelector('form');
  if (questionForm) {
    questionForm.addEventListener('submit', function (event) {
      event.preventDefault();
      const userInput = document.getElementById("question").value;

      fetch('/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput })
      })
      .then(response => response.json())
      .then(data => {
        document.getElementById("response").innerText = data.reply;
      })
      .catch(error => {
        console.error('Error:', error);
        document.getElementById("response").innerText = "An error occurred. Please try again.";
      });
    });
  }
});
