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
      // Display bot message when image is received successfully
      displayBotMessage('Image received! 🖼️', 'photo_camera');
    })
    .catch(error => {
      console.log('Error sending image:', error);
      alert('Something went wrong while uploading the image.');
    });

    cameraContainer.style.display = 'none';  // Close the camera container after capturing
  });

  // Send user message and get Groq response
  sendBtn.addEventListener('click', function () {
    const userMessage = textInput.value.trim();
    if (userMessage === '') return;

    // Display user message in the chatbox
    displayUserMessage(userMessage);

    // Send user message to the backend for processing
    fetch('/groq-response', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: userMessage }),
    })    
    .then(response => response.json())
    .then(data => {
      // Display bot's reply
      displayBotMessage(data.reply, 'heart_plus');
    })
    .catch(error => {
      console.log('Error receiving Groq response:', error);
      // Display error message if something went wrong
      displayBotMessage('Oops! Something went wrong. Please try again later.', 'error');
    });

    textInput.value = '';  // Clear input field after sending
  });

  // Helper function to display the user's message in the chatbox
  function displayUserMessage(message) {
    const outgoingMsg = document.createElement('li');
    outgoingMsg.className = 'chat outgoing';
    outgoingMsg.innerHTML = `<p>${message}</p>`;
    chatBox.appendChild(outgoingMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Helper function to display the bot's message in the chatbox
  function displayBotMessage(message, icon) {
    const botMsg = document.createElement('li');
    botMsg.className = 'chat incoming';
    botMsg.innerHTML = `<span class="material-symbols-outlined">${icon}</span>
                        <p>${message}</p>`;
    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Enable "Enter" to send the message (without shift key)
  textInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendBtn.click();
    }
  });

  // Toggle settings dropdown when the settings button is clicked
  settingsBtn.addEventListener('click', function () {
    settingsDropdown.classList.toggle('show');
  });

  // Close settings dropdown if clicked outside
  window.addEventListener('click', function (event) {
    if (!settingsBtn.contains(event.target) && !settingsDropdown.contains(event.target)) {
      settingsDropdown.classList.remove('show');
    }
  });

  // Function to handle submitting the question via form (added here)
  function submitQuestion(event) {
    event.preventDefault();  // Prevent the default form submission
    
    const userInput = document.getElementById("question").value;  // Get user input

    // Send the user input to the Flask backend
    fetch('/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userInput })  // Send the input as JSON
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
      document.getElementById("response").innerText = data.reply;  // Display the response
    })
    .catch(error => {
      console.error('Error:', error);
      document.getElementById("response").innerText = "An error occurred. Please try again.";
    });
  }

  // Attach the submitQuestion function to the form (if it exists in the HTML)
  const questionForm = document.querySelector('form');
  if (questionForm) {
    questionForm.addEventListener('submit', submitQuestion);
  }
});
