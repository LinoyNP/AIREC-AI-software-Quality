# AIREC 

**AIREC** is an advanced **code analysis tool** designed to evaluate submitted code based on three core principles:
![AIREC Logo](static/icons/p.png)
---

## 🌟 Core Principles

| Principle      | Description |
|----------------|-------------|
| 🔒 **Security** | Detect potential vulnerabilities and protect the code from threats. |
| ✅ **Correctness** | Ensure the code performs exactly as intended. |
| 📝 **Readability** | Evaluate clarity, structure, and maintainability. |

---

## 💡 Highlights

- Automatic code review for both **AI-generated** and **human-written** code.  
- Supports multiple programming languages and paradigms.  
- Provides actionable insights to improve code quality efficiently.  

## 📚 How to Use
🔧 **JavaScript Setup (Frontend)**
To run this project locally, first clone the repository using git clone https://github.com/LinoyNP/AIREC-AI-software-Quality.git and navigate into the project folder. 
Make sure Node.js is installed, then run npm install to install all dependencies. 
Create a .env file in the root directory and add your Firebase credentials using the following format: VITE_FIREBASE_API_KEY=your_api_key, VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com, VITE_FIREBASE_PROJECT_ID=your_project_id, VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com, VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id, and VITE_FIREBASE_APP_ID=your_app_id. Once the environment variables are set, start the development server with npm run dev, and the app will be available at http://localhost:5000

🐍 **Python Setup (Backend)**
To install the required Python packages, this project uses a two-step dependency management system with requirements.in and requirements.txt. The requirements.in file contains the high-level dependencies you define manually. To generate a pinned requirements.txt file with exact versions, run:
pip install pip-tools
pip-compile requirements.in
Then, install all dependencies with:
 pip install -r requirements.txt. 
 This ensures consistent environments across machines and makes it easier to manage updates.
---