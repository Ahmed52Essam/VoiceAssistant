# 🎙️ Python Voice Assistant

A fully offline, voice-activated assistant ```built with Python```. It uses ```Vosk for speech recognition and pyttsx3 for text-to-speech```, enabling you to open apps, type text, take screenshots, and more — all hands-free.

---

## 🧠 Overview

This voice assistant:
- Listens to your voice using your default microphone
- Recognizes spoken commands using the Vosk speech recognition model
- Executes a variety of system-level commands using Python automation tools
- Speaks responses back to you using `pyttsx3`

> All operations are **offline** and private — no internet or cloud APIs required.

---

## ✨ Features

- 🔈 Speak commands, get voice feedback
- 🗃️ Open apps like Notepad or Calculator
- 💻 Minimize, maximize, or close windows
- 🖼️ Show images
- 📋 Copy & paste using voice
- 🔍 Google search using speech
- 📷 Take screenshots
- 🔠 Type dictated text

## 🧰 Prerequisites
Before running this project, make sure you have:

Python 3.8 or higher installed on your system
You can download it from [python.org](https://www.python.org/downloads/)

To verify Python is installed, run in your terminal or command prompt: ``` python --version```

## ⚙️ Setup Instructions
1- Open the cmd or the terminal in the project directory and paste this command: pip install -r requirements.txt

2-  Download Vosk model (No need it is uploaded within the repo)

Download the English model from:
https://alphacephei.com/vosk/models

we are using a light weight variant of the vosk model: "vosk-model-small-en-us-0.15"

3- You are all set , Run the assistant !
either by pasting this command in the terminal: python main.py
or
double clicking the main.py file

## 🗣️ Supported Voice Commands

| Command            | Action                           |
| ------------------ | -------------------------------- |
| "open notepad"     | Launches Notepad                 |
| "open calculator"  | Launches Calculator              |
| "take screenshot"  | Saves a screenshot to file       |
| "show image"       | Opens `image.jpg`                |
| "copy this text"   | Copies predefined text           |
| "paste clipboard"  | Pastes clipboard content         |
| "type hello world" | Types "hello world"              |
| "search for cats"  | Opens browser, searches for cats |
| "close window"     | Prompts to close active window   |
| "exit"             | Gracefully exits the program     |


## 📦 Dependencies

vosk

pyttsx3

sounddevice

pyautogui

pyperclip

Pillow

webbrowser (built-in)

os (built-in)

Use pip install -r requirements.txt to install them all.

## 📁 File Structure

voice-assistant\
│\
├── main.py                         # Entry point   \
├── vosk-model-small-en-us-0.15/    # Speech recognition model  \
├── image.jpg                       # Used in "show image"  \
├── requirements.txt                # Dependencies  \
├── README.md                       # You are here


## 👤 Author
Created by Ahmed Essam Sayed    \
ahmed52essam@gmail.com

Feel free to contact me for support or in case needed Access to GitHub Repository