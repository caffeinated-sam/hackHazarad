document.addEventListener('DOMContentLoaded', function () {
  const chatBox = document.querySelector('.chatbox');
  const sendBtn = document.querySelector('.chat-input span.material-symbols-outlined:last-of-type');
  const textInput = document.querySelector('.chat-input textarea');
  const fileUploadInput = document.getElementById('fileUpload'); // Hidden image input (used in old logic)
  const uploadImage = document.getElementById('uploadImage');     // New image input from dropdown
  const uploadPDF = document.getElementById('uploadPDF');         // New PDF input from dropdown

  const settingsBtn = document.getElementById('settings-btn');
  const settingsDropdown = document.getElementById('settings-dropdown');

  const imagePreviewContainer = document.getElementById('imagePreviewContainer');
  const imagePreview = document.querySelector('#imagePreview img');
  const removeImageBtn = document.getElementById('removeImageBtn');

  const uploadMenuBtn = document.getElementById('uploadMenuBtn');
  const uploadMenu = document.getElementById('uploadMenu');

  let selectedImageFile = null;

  // === Upload Dropdown Menu Logic ===
  uploadMenuBtn.addEventListener('click', () => {
    uploadMenu.style.display = uploadMenu.style.display === 'flex' ? 'none' : 'flex';
  });

  window.addEventListener('click', function (e) {
    if (!uploadMenuBtn.contains(e.target) && !uploadMenu.contains(e.target)) {
      uploadMenu.style.display = 'none';
    }
  });

  // Trigger old image upload logic
  uploadImage.addEventListener('change', function () {
    fileUploadInput.files = uploadImage.files;
    fileUploadInput.dispatchEvent(new Event('change'));
  });

  // Handle PDF Upload
  uploadPDF.addEventListener('change', function () {
    const file = uploadPDF.files[0];
    if (!file) return;

    const li = document.createElement('li');
    li.className = 'chat outgoing';
    li.innerHTML = `<p>📄 Uploaded PDF: ${file.name}</p>`;
    chatBox.appendChild(li);
    chatBox.scrollTop = chatBox.scrollHeight;

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload-pdf', {
      method: 'POST',
      body: formData
    })
      .then(res => res.json())
      .then(data => displayBotMessage(data.response || "✅ PDF received!", 'description'))
      .catch(err => {
        console.error(err);
        displayBotMessage("⚠️ PDF upload failed.", 'error');
      });

    uploadPDF.value = '';
  });

  // === Image Upload + Preview Logic ===
  fileUploadInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;

    selectedImageFile = file;

    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.src = e.target.result;
      imagePreviewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
  });

  removeImageBtn.addEventListener('click', function () {
    selectedImageFile = null;
    imagePreview.src = '';
    imagePreviewContainer.style.display = 'none';
    fileUploadInput.value = '';
  });

  // === Message Sending Logic ===
  sendBtn.addEventListener('click', handleSendMessage);
  textInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  });

  async function handleSendMessage() {
    const userMessage = textInput.value.trim();
    if (userMessage === '' && !selectedImageFile) return;

    const li = document.createElement('li');
    li.className = 'chat outgoing';
    li.style.display = 'flex';
    li.style.flexDirection = 'column';
    li.style.alignItems = 'flex-end';

    if (selectedImageFile) {
      const img = document.createElement('img');
      img.src = imagePreview.src;
      img.alt = 'Uploaded Image';
      img.style.maxWidth = '200px';
      img.style.borderRadius = '10px';
      img.style.marginBottom = '8px';
      li.appendChild(img);
    }

    if (userMessage) {
      const caption = document.createElement('p');
      caption.style.whiteSpace = 'pre-wrap';
      caption.textContent = userMessage;
      li.appendChild(caption);
    }

    chatBox.appendChild(li);
    chatBox.scrollTop = chatBox.scrollHeight;

    if (selectedImageFile) {
      const formData = new FormData();
      formData.append('file', selectedImageFile);
      formData.append('caption', userMessage);

      try {
        const response = await fetch('/upload-image', {
          method: 'POST',
          body: formData
        });

        const data = await response.json();
        if (data.response) {
          displayBotMessage(data.response, 'image');
        } else {
          displayBotMessage("❌ Failed to get a response for the image.", 'error');
        }
      } catch (err) {
        console.error('Upload error:', err);
        displayBotMessage("⚠️ Upload failed. Please try again.", 'error');
      }

    } else if (userMessage) {
      fetch('/groq-response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage })
      })
        .then(res => res.json())
        .then(data => displayBotMessage(data.reply, 'heart_plus'))
        .catch(() => displayBotMessage("Something went wrong. Please try again.", 'error'));
    }

    textInput.value = '';
    resetTextarea();
    selectedImageFile = null;
    imagePreview.src = '';
    imagePreviewContainer.style.display = 'none';
    fileUploadInput.value = '';
  }

  function resetTextarea() {
    textInput.style.height = 'auto';
    textInput.style.overflowY = 'hidden';
  }

  textInput.addEventListener('input', function () {
    const maxHeight = 200;
    textInput.style.height = 'auto';
    textInput.style.height = Math.min(textInput.scrollHeight, maxHeight) + 'px';
    textInput.style.overflowY = textInput.scrollHeight > maxHeight ? 'auto' : 'hidden';
  });

  function displayBotMessage(message, icon) {
    const typingIndicator = document.createElement('li');
    typingIndicator.className = 'chat incoming typing';
    typingIndicator.innerHTML = `
      <span class="material-symbols-outlined">${icon}</span>
      <p class="typing-dots">Typing</p>
    `;
    chatBox.appendChild(typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight;

    setTimeout(() => {
      typingIndicator.remove();

      const botMsg = document.createElement('li');
      botMsg.className = 'chat incoming';

      const span = document.createElement('span');
      span.className = 'material-symbols-outlined';
      span.innerText = icon;

      const p = document.createElement('p');
      p.style.whiteSpace = 'pre-wrap';

      botMsg.appendChild(span);
      botMsg.appendChild(p);
      chatBox.appendChild(botMsg);

      let index = 0;
      const typingSpeed = 5;

      function typeChar() {
        if (index < message.length) {
          p.innerHTML += message[index] === '\n' ? '<br>' : message[index];
          index++;
          setTimeout(typeChar, typingSpeed);
        } else {
          chatBox.scrollTop = chatBox.scrollHeight;
        }
      }

      typeChar();
    }, 500);
  }

  // === Settings Button Toggle ===
  const settingsMenu = document.getElementById('settings-menu');

// Toggle settings dropdown
settingsBtn.addEventListener('click', () => {
  settingsMenu.style.display = settingsMenu.style.display === 'flex' ? 'none' : 'flex';
});

// Hide when clicking outside
window.addEventListener('click', function (e) {
  if (!settingsBtn.contains(e.target) && !settingsMenu.contains(e.target)) {
    settingsMenu.style.display = 'none';
  }
});

  // === Optional fallback form ===
  const questionForm = document.querySelector('form');
  if (questionForm) {
    questionForm.addEventListener('submit', function (event) {
      event.preventDefault();
      const userInput = document.getElementById("question").value;

      fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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
