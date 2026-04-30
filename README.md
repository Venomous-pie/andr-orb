<div align="center">

# andr-orb

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](#)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blueviolet.svg)](#)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#)

**A floating desktop AI assistant. It lives in an orb on your screen. You can drag it, chat with it, and hear it speak.**

</div>

## Features

andr-orb is a clear, floating orb that always stays on top of your windows. It gives you quick access to an AI assistant right from your desktop. It is lightweight, stays out of your way, and can speak to you.

* **Floating Orb Interface:** A clear, glowing orb that you can click and drag anywhere on your screen. It always stays on top of other windows.
* **Expandable Chat Panel:** Double-click the orb to open a chat window. You can change its size and read your past messages. You can hide it back into the orb at any time.
* **Smart Conversations:** It uses the Groq API to chat with you. It remembers your chat history so it can give better answers.
* **Voice Responses:** The assistant speaks every reply out loud using Microsoft Edge text-to-speech.
* **Thinking Animation:** The orb pulses with a glow when the AI is thinking. This shows you that it is working on an answer.
* **Startup Greeting:** When you open the app, the assistant will create and speak a custom hello message.
* **Auto-Restart for Developers:** A built-in tool (`run.py`) watches your Python files. If you change the code, the app will restart automatically.

## Installation Guide

Follow these simple steps to install andr-orb on your computer.

### What You Need

* **Python 3.10 or newer**
* **pip** (Python package installer)
* **A Groq API Key** (You can get one for free at [console.groq.com](https://console.groq.com))

### Step 1: Get the Code

```bash
git clone https://github.com/Venomous-pie/andr-orb.git
cd andr-orb
```

### Step 2: Create a Virtual Environment

It is best to install Python packages in a virtual environment.

```bash
python -m venv .venv
```

Activate the virtual environment:

* **For Windows:**
  ```bash
  .venv\Scripts\activate
  ```
* **For Linux and macOS:**
  ```bash
  source .venv/bin/activate
  ```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Configuration

Create a new file named `config.py` in the main folder.

Add this code to the file:

```python
GROQ_API_KEY = "your-groq-api-key-here"
GROQ_MODEL   = "llama-3.3-70b-versatile"

ORB_SIZE     = 60
PANEL_WIDTH  = 380
PANEL_HEIGHT = 520
```

| Setting | What it does |
|---|---|
| `GROQ_API_KEY` | Your secret API key from Groq. |
| `GROQ_MODEL` | The AI model you want to use for chatting. |
| `ORB_SIZE` | The size of the floating orb in pixels. |
| `PANEL_WIDTH` | The starting width of the chat panel in pixels. |
| `PANEL_HEIGHT` | The starting height of the chat panel in pixels. |

### Step 5: Run the App

```bash
python main.py
```

If you are a developer and want the app to restart when you edit code, run this instead:

```bash
python run.py
```

> **Note:** The `run.py` file works best on Linux and macOS. If you use Windows, you should run `python main.py` directly.

## How to Use

1. **Start the app.** The orb will appear near the bottom-right corner of your screen and say hello.
2. **Double-click the orb** to open the chat panel.
3. **Type a message** in the text box and press `Enter` or click `Send`.
4. **Wait for the answer.** The orb will pulse while thinking. Then, the answer will appear in the chat and play out loud.
5. **Hide the panel** by clicking the `−` button at the top. The panel will turn back into the orb.
6. **Drag the orb** to move it anywhere on your screen.
7. **Resize the panel** by dragging its edges or corners.

## Project Structure

```
andr-orb/
│
├── main.py          # Starts the app and connects everything together
├── orb.py           # Creates the floating orb, animation, and drag actions
├── panel.py         # Creates the chat window and text input
├── brain.py         # Connects to the Groq API and remembers chat history
├── voice.py         # Makes the app speak using text-to-speech
├── run.py           # Auto-restarts the app when you change the code
├── config.py        # Your secret keys and settings (you create this)
├── requirements.txt # List of Python packages needed to run the app
├── .gitignore       # Tells Git what files to ignore
└── README.md        # This help document
```

## Advanced Settings

You can change the `config.py` file to make the app look and act differently:

```python
# Required Settings
GROQ_API_KEY = "your-groq-api-key-here"
GROQ_MODEL   = "llama-3.3-70b-versatile"

# Optional UI Settings
ORB_SIZE     = 60     # Orb size in pixels
PANEL_WIDTH  = 380    # Chat panel starting width
PANEL_HEIGHT = 520    # Chat panel starting height
```

You can also change the voice. Open the `voice.py` file and find this line:

```python
communicate = edge_tts.Communicate(text, voice="en-US-AndrewNeural", rate="+30%")
```

Replace `"en-US-AndrewNeural"` with any voice name from [edge-tts](https://github.com/rany2/edge-tts).

## Contributing

1. Fork the Project
2. Create a Feature Branch (`git checkout -b feature/your-feature`)
3. Commit Changes (`git commit -m "Add your feature"`)
4. Push to Branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project does not have a license file yet.
If you have questions about using this code, please contact the repository owner at [Venomous-pie/andr-orb](https://github.com/Venomous-pie/andr-orb).

&copy; 2025 [Venomous-pie](https://github.com/Venomous-pie). All Rights Reserved.
