# Universal Music Player

A sleek, modern desktop audio and video player built with Python, CustomTkinter, and the universal VLC media engine. Supports `.mp3`, `.mp4`, `.m4a`, `.wav`, `.aac`, `.flac`, and more!

## ✨ Features
- **All-Format Engine:** Uses native VLC decoders to play advanced formats like Apple's `.m4a` and standard video formats.
- **Modern Dark UI:** Interactive layout built using `customtkinter` with custom status bars.
- **Queue Sidebar:** Easily select multiple files to load a custom playlist queue on the fly.
- **Progress Control:** Seek through media tracks smoothly with a real-time tracking slider.

## 🚀 How to Run Locally

### Prerequisites
1. Install [VLC Media Player](https://videolan.org) on your computer (required for the underlying audio decoders).
2. Install the necessary Python packages:
   ```bash
   pip install customtkinter python-vlc
   ```

### Running the App
Navigate to the directory and execute:
```bash
python player.py
```

## 🛠️ Compiling to a Standalone Executable (.exe)
To package this app into a single `.exe` file for Windows:
```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole player.py
```
Find the finished executable inside the newly created `dist/` directory!
