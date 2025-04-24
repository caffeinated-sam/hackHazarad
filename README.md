![github-submission-banner](https://github.com/user-attachments/assets/a1493b84-e4e2-456e-a791-ce35ee2bcf2f)

# 🚀 Project Title

## Healthcare Ai

---

## 📌 Problem Statement

 
### **Problem Statement 1: Weave AI magic with Groq**

---

## 🎯 Objective

### Healthcare Ai is designed to solve a critical problem in the healthcare space: **making medical information more accessible and understandable to everyday users** through AI-powered assistance.

---

### ✅ **Problem Solved**
Patients often receive prescriptions, reports, or medication packaging with complex terminology or lack of detailed explanations. Understanding what a medicine is used for, its possible side effects, or interacting conditions can be overwhelming without a medical background.

---

### 👩‍⚕️ **Who It Serves**
- **Patients & Caregivers**: who want quick, understandable explanations about medicines or health-related documents.
- **Pharmacists/Health Workers in Remote Areas**: who may lack detailed references on new medications.
- **Elderly Users**: who may struggle with reading or comprehending medical documents.

---

### 🌍 **Real-World Use Case**
A user uploads a photo of a medicine strip or a scanned doctor’s prescription. The chatbot:
- Detects the medicine name using OCR and AI
- Retrieves its use-case by searching a local medicine PDF
- Explains it in simple, natural language using LLM (like LLaMA via GROQ)

Users can also ask follow-up questions about the same medicine without re-uploading.

---

### 💡 **Value Provided**
- **Saves time** in researching medications
- **Improves understanding** of treatment plans
- **Increases accessibility** for those without immediate access to a doctor or pharmacy.

---

## 🧠 Team & Approach

### Team Name:  
#### `NOCTURNUM`

### Team Members:  
- Rudresh Kumar ([GitHub](https://github.com/MONSTER4REX) / [LinkedIn](https://www.linkedin.com/in/rudresh-kumar-197169320/) / Team Leader/Database)  
- Samridh Srivastava ([GitHub](https://github.com/caffeinated-sam) / [LinkedIn](https://www.linkedin.com/in/samridh-srivastava-14443b31b/) / Frontend)
- Jay Varshney ([GitHub](https://github.com/Jay-Varshney) / [LinkedIn](https://www.linkedin.com/in/jay-varshney-a56380320/) / Frontend)
- Shagun Goyal (GitHub / LinkedIn / Backend)

### Your Approach:  

---

### 💭 **Why We Chose This Problem**
Access to clear and trustworthy medical information is a universal need. Yet, many people struggle to understand prescriptions, medicine labels, or how to use a medication properly — especially in regions with limited healthcare access or language barriers. We wanted to **bridge this gap using AI** — making health info more accessible, safer, and easier to understand with just an image or a simple question.

---

### 🔧 **Key Challenges We Addressed**
- **Image-to-Text Accuracy**: Extracting reliable medicine names using OCR (with Tesseract) from various image qualities and fonts.
- **Relevant Context Extraction**: Searching a large medicine PDF quickly to find accurate, concise info (using FAISS + embedding search).
- **Natural Language Understanding**: Making the AI provide helpful responses **only based on trusted context**, not hallucinations.
- **UI Simplicity**: Ensuring users could just upload a photo or document and get answers — no tech knowledge required.

---

### 🔄 **Pivots, Brainstorms, & Breakthroughs**
- Initially planned to use **real-time camera input**, but pivoted to **file uploads** to improve accuracy and user experience.
- Switched from OpenAI to **GROQ's LLaMA3** for faster and cost-effective inference.
- Brainstormed how to serve users in **low-bandwidth areas** with minimal UI and offline PDF-based RAG pipeline.

---

## 🛠️ Tech Stack

### Core Technologies Used:
---

#### 🖥️ **Frontend**  
- **HTML/CSS/JS** – For chatbot layout, responsive design, and user interaction  
- **Vanilla JavaScript** – Handling file uploads, dynamic UI, chat rendering  
- **Material Symbols & Google Fonts** – UI icons and typography  
- **Responsive Design** – Optimized for both desktop and mobile

---

#### 🧠 **Backend**  
- **Flask (Python)** – Lightweight server handling API routes  
- **LangChain + FAISS** – For document-based Retrieval-Augmented Generation (RAG)  
- **Tesseract OCR** – Extracts medicine names from images using pytesseract  
- **GROQ API (LLaMA3)** – For fast and cost-effective natural language responses 

---

#### 🗃️ **Database**  
- **Local File Storage** – For uploaded images and PDFs  
- (Optional) **FAISS Vector Store** – For embedding and fast context retrieval

---

#### 🔗 **APIs**  
- **GROQ API** – Chat completion with LLaMA3  
---

#### ☁️ **Hosting**  
- **PythonAnywhere / Render (Optional)** – Deployable with slight configuration    
- **Ubuntu/Linux & Windows** – Cross-platform testing

---

### Sponsor Technologies Used (if any):
- [✅] **Groq:** How we used Groq:
                - We integrated **Groq’s LLaMA 3 model** through their blazing-fast API to power the chatbot’s conversational intelligence. <br /> 
                - The chatbot leverages Groq for **real-time medical Q&A**, offering explanations about medicines extracted from uploaded images and documents.<br />
                - We used Groq’s **chat completion endpoint** with a custom system prompt that ensures responses are grounded in medical context.<br />
                - The performance advantage of Groq helped us **reduce latency significantly**, making the chatbot feel responsive and reliable.<br />

> _Groq was crucial in delivering fast and context-aware medical responses for an AI healthcare assistant._

--- 
- [ ] **Monad:** _Your blockchain implementation_  
- [ ] **Fluvio:** _Real-time data handling_  
- [ ] **Base:** _AgentKit / OnchainKit / Smart Wallet usage_  
- [ ] **Screenpipe:** _Screen-based analytics or workflows_  
- [ ] **Stellar:** _Payments, identity, or token usage_
---

## ✨ Key Features


✅ Image-Based Medicine Recognition
→ Users can upload an image of a medicine strip or label, and the chatbot automatically extracts the name using OCR and identifies its use from medical resources.

✅ Document (PDF/DOCX) Understanding
→ Upload a medical prescription or document, and the chatbot intelligently processes the content to answer questions based on it.

✅ Groq-Powered Fast & Contextual Responses
→ Uses the ultra-fast Groq LLM to provide accurate, relevant, and real-time answers—minimizing latency and enhancing user experience.

✅ Multi-Modal Chat Interface
→ A clean, modern chat UI supporting text, image, and file input with preview support, persistent history, and intuitive interaction.


---

## 📽️ Demo & Deliverables

- **Demo Video Link:** [[YouTube link ](https://www.youtube.com/watch?v=ksiyXk6G9nk)]  
- **Pitch Deck / PPT Link:** [[Google Slides](https://docs.google.com/presentation/d/13EBZAqgq57nVgSsTIZPdPxhDz1Xb3C37NT66u9SaJUI/edit?usp=sharing)]  

---

## ✅ Tasks & Bonus Checklist

- [✅] **All members of the team completed the mandatory task - Followed at least 2 of our social channels and filled the form** (Details in Participant Manual)  
- [✅] **All members of the team completed Bonus Task 1 - Sharing of Badges and filled the form (2 points)**  (Details in Participant Manual)
- [✅] **All members of the team completed Bonus Task 2 - Signing up for Sprint.dev and filled the form (3 points)**  (Details in Participant Manual)

*(Mark with ✅ if completed)*

---

## 🧪 How to Run the Project

### Requirements:
- Python
- GroqAPI Key in Ai/Config.py

### Local Setup:
```bash
# Clone the repo
git clone https://github.com/your-team/project-name

# Install dependencies
cd project-name
pip install -r requirements
python -m venv venv 
.\venv\Scripts\Activate
pip install -r requirements
deactivate 
python -m venv faiss
.\faiss\Scripts\activate
Pip install -r requirements.txt


# Start development server
flask run 
```

Provide any backend/frontend split or environment setup notes here :

-Install Tesseract <br /> 
-Install to the default path (e.g. C:\Program Files\Tesseract-OCR) <br /> 
-During install, make sure to check the box that says “Add to PATH” <br /> 
-If not automatically added, go to: <br /> 

 System Properties > Environment Variables > PATH
 Add this:

 makefile
 ```bash
 C:\Program Files\Tesseract-OCR
```
---

## 🧬 Future Scope

List improvements, extensions, or follow-up features:

- 📈 More Integrations: 

   Add support for voice input, EMR systems, or pharmacy APIs for real-time drug data.

- 🛡️ Security Enhancements:

   Implement user authentication, role-based access, and encrypted file handling to protect sensitive medical information.

- 🌐 Localization / Accessibility:

   Multilingual support and screen reader optimization to serve diverse user bases, especially in underserved regions.
---

## 📎 Resources / Credits

🧠 APIs & Datasets Used:
   - Groq API – for blazing-fast responses using the LLaMA-3 model.
   - Tesseract OCR – for extracting text from medicine images.
   - PyMuPDF (fitz) / python-docx – for parsing PDFs and DOCX medical documents.
   - Custom Dataset (medicine uses) – a curated PDF used as a base knowledge context.

🔧 Open Source Libraries / Tools:
    - LangChain – for context handling and chaining document queries.
    - Flask – backend web framework.
    - OpenCV – for image preprocessing before OCR.
    - JavaScript (Vanilla) – for frontend interactivity.
    - HTML/CSS – for UI design.

🙌 Acknowledgements:
    - OpenAI / Groq teams for making advanced LLM APIs accessible.
    - Tesseract OCR community for maintaining high-quality open OCR.
    - Hackathon mentors / organizers for guidance and feedback.
    - Stack Overflow & GitHub – for all the late-night bug fixes 🐛💡

---

### 🏁 Final Words

What a ride! 🚀  
From brainstorming at midnight to debugging right before the deadline, this hackathon was packed with challenges, breakthroughs, and caffeine-fueled coding sprints.

💡 **Key Learnings:**
- Integrating OCR and LLMs is super powerful — but also tricky!
- We learned how to optimize user experience by balancing speed and functionality.
- Working with Groq's blazing-fast API was a game-changer for LLM responsiveness.

⚔️ **Challenges Faced:**
- Handling long PDF contexts efficiently.
- Getting image uploads to talk to OCR + GPT without lag.
- Making the chatbot feel helpful *and* responsive under time pressure.

😂 **Fun Moments:**
- Watching the chatbot “hallucinate” answers before we got context right.
- Everyone fumbling PowerShell commands multiple times.
- Accidentally uploading a selfie instead of a pill image 🤦‍♂️
- Realizing the dark theme looked *too* good to change 😎

🙏 **Shout-outs:**
To the mentors, teammates, and fellow hackers — thank you for the inspiration and camaraderie. This was more than just building a project — it was about pushing limits, learning fast, and having fun!

Onward to more hacks and bigger ideas! 💻🔥

---
