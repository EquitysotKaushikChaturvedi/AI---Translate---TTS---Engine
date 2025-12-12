# Hybrid Neural Translation & TTS Engine

## 📌 Project Overview
This project is an enterprise-grade **Hybrid Translation & Text-to-Speech (TTS) System**. It combines the superior quality of Cloud Neural Voices with the reliability of Offline System Audio.

It is designed to be a **100% Free** alternative to paid APIs like Google Cloud, offering a robust "Google Translate" like experience that works even when the internet is unstable.

## 🎥 Demo & Screenshots
**[View Live Demo Recording & Screenshots (Google Drive)](https://drive.google.com/file/d/1VsOtLUWpCZuRv7-qUasSq9jc-eblLhDE/view?usp=sharing)**

### 🚀 Key Capabilities
*   **Hybrid TTS Engine (Auto-Switching)**:
    *   **Online Mode (Primary)**: Streams **Neural Voices** (Human-like) from Microsoft Edge servers via `edge-tts`.
    *   **Offline Mode (Fallback)**: Automatically switches to **System Voices** (Robotic) via `pyttsx3` if the internet fails.
*   **Neural Audio Quality**: Access to high-end voices like "Swara" (Hindi), "Jenny" (US English), and "Neerja" (Indian English).
*   **Real-time Translation**: Powered by `deep-translator` (Google Translate wrapper).
*   **Indian Language Focus**: Enhanced support for Hindi, Bengali, Tamil, Telugu, Marathi, etc.

---

## 🛠️ Technology Stack & Logic

### 1. The TTS Engine (`gcloud_client.py`)
The system uses a smart **Try-Catch Fallback** mechanism:

1.  **Step 1 (Neural)**: The app attempts to connect to `edge-tts`.
    *   *Input*: "Namaste"
    *   *Action*: Request `hi-IN-SwaraNeural` audio.
    *   *Result*: High-quality MP3 streamed to the user.
2.  **Step 2 (Offline)**: If Step 1 fails (Connection Error/Timeout):
    *   *Action*: The app catches the error.
    *   *Fallback*: It invokes `pyttsx3` (Python Text-to-Speech).
    *   *Result*: Generates a standard `.wav` using your computer's built-in voice (SAPI5 on Windows).

### 2. The Translator
*   **Library**: `deep-translator`.
*   **Logic**: Scrapes the Google Translate web interface to provide free translations for over 100 languages.

---

## 📂 Project Structure

```text
flask-gcloud-translate-tts 2/
├── backend/               # PYTHON LOGIC
│   ├── app.py             # Main Server
│   ├── gcloud_client.py   # Hybrid Engine
│   └── requirements.txt   # Dependencies
├── frontend/              # USER INTERFACE
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
├── run_local.sh           # Installer Script
└── DEPLOYMENT.md          # Deployment Guide
```

---

## 📥 Installation & Setup

### Prerequisites
*   **Python 3.8+** installed.
*   **Internet**: Recommended for Neural Voices (but works Offline too).

### Step-by-Step
1.  **Run the Installer**:
    ```bash
    ./run_local.sh
    ```
    (Double-click `run_local.sh` on Windows).
2.  **Open in Browser**:
    Go to `http://127.0.0.1:5000`.

---

## 🔌 API Reference for Developers

### Generate Audio (TTS)
*   **Endpoint**: `POST /tts`
*   **JSON Body**:
    ```json
    {
      "text": "Hello World",
      "lang": "en-US"
    }
    ```
*   **Logic**: Returns Neural MP3 if online, System WAV if offline.

---

## 👨‍💻 Credits
*   **Developed By**: Kausik
*   **Powered By**: Microsoft Edge (Neural TTS) & Google Translate.
