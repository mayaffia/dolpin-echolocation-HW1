# Installation and Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Quick Start

### Option 1: Using the startup scripts (Recommended)

#### On macOS/Linux:

```bash
cd gui_app
chmod +x run.sh
./run.sh
```

#### On Windows:

```cmd
cd gui_app
run.bat
```

### Option 2: Manual installation

1. **Create a virtual environment** (recommended):

```bash
cd gui_app
python3 -m venv venv
```

2. **Activate the virtual environment**:

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```cmd
venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Start the server**:

```bash
cd backend
python server.py
```

5. **Open your browser** and navigate to:

```
http://localhost:5000
```

## Troubleshooting

### Port already in use

If port 5000 is already in use, edit `backend/server.py` line 349:

```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)  # Change port here
```

### Module not found: dolphin

The server automatically adds the `ifraimova` directory to the Python path. Ensure the directory structure is:

```
HW1/
├── ifraimova/
│   └── dolphin.py
└── gui_app/
    └── backend/
        └── server.py
```

### Virtual environment issues

If you encounter issues with the virtual environment, try:

```bash
rm -rf venv  # Remove old venv
python3 -m venv venv  # Create new venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Browser compatibility

The application requires a modern browser with JavaScript enabled and WebSocket support. If you experience issues:

- Clear browser cache
- Try a different browser
- Check browser console for errors (F12)

## Verifying Installation

After starting the server, you should see:

```
======================================================================
Dolphin Echolocation GUI Server
======================================================================
Server starting on http://localhost:5000
Open your browser and navigate to http://localhost:5000
======================================================================
```

The browser should display a GUI with:

- Menu bar at the top
- Toolbar with buttons
- Left panel with parameters
- Center canvas for visualization
- Right panel with progress information
- Status bar at the bottom

## Next Steps

Once installed, refer to `README.md` for usage instructions.
