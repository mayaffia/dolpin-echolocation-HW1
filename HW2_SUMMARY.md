# HW2: Dolphin Echolocation Optimization - GUI Application

## Project Overview

This project implements a comprehensive desktop GUI application for the Dolphin Echolocation metaheuristic optimization algorithm, fulfilling all requirements for **Track 2a, Grade 8**.

## Implementation Details

### Architecture: Client-Server Application

**Backend (Python):**

- Framework: Flask with Flask-SocketIO for real-time communication
- Algorithm: Extended DolphinEcholocation class with step-by-step execution capability
- Location: `gui_app/backend/server.py`

**Frontend (JavaScript):**

- Visualization: Plotly.js for interactive 2D plots
- Communication: Socket.IO for WebSocket connections
- UI: Responsive desktop application design
- Location: `gui_app/frontend/`

## Requirements Fulfilled

### ✅ Track 2a - Grade 6 Requirements

1. **Core Metaheuristic Implementation**
   - Full Dolphin Echolocation Algorithm from HW1
   - Located in `ifraimova/dolphin.py`
   - Extended with step-by-step execution in `gui_app/backend/server.py`

2. **GUI with Canvas**
   - Large canvas area for 2D function visualization
   - Interactive contour plots with color mapping
   - Real-time updates during optimization

3. **Function Selection**
   - Dropdown list with 3 test functions:
     - Sphere Function: f(x) = Σ(xi²)
     - Rastrigin Function: f(x) = 10n + Σ(xi² - 10cos(2πxi))
     - Rosenbrock Function: f(x) = Σ(100(xi+1 - xi²)² + (1-xi)²)

4. **Variable Control System**
   - Sliders for each variable dimension (dynamically generated)
   - Text boxes synchronized with sliders (bidirectional)
   - Checkbox selection for 2 variables to visualize in 2D
   - Only 2 checkboxes can be selected simultaneously
   - Other variables become constants (fixed by slider values)

5. **Solution Visualization**
   - Best solution marked with yellow star on 2D plot
   - Solution coordinates displayed in right panel
   - Real-time updates as optimization progresses

### ✅ Track 2a - Grade 8 Additional Requirements

1. **Parameter Configuration Panel**
   - Always visible panel (not a dialog box)
   - Configurable parameters:
     - Number of agents (population size): 5-100
     - Maximum iterations: 10-500
     - Function dimension: 2-20
   - Located in left panel of GUI

2. **Step-by-Step Visualization**
   - **Start Button**: Runs optimization continuously
   - **Step Button**: Executes one iteration at a time
   - **Stop Button**: Pauses execution at any point
   - Real-time visualization updates after each step

3. **Agent Position Visualization**
   - Current positions: White circles with black borders
   - Agent numbers: Displayed as text (0, 1, 2, ...)
   - Best solution: Yellow star with black border
   - Clearly distinguishable on the plot

4. **Agent Trajectories**
   - Dashed lines connecting previous positions to current positions
   - Toggle on/off with checkbox
   - Shows last 10 positions for each agent
   - Semi-transparent white lines for clarity

### ✅ Additional GUI Components

1. **Menu Bar**
   - File, Edit, View, Help menus
   - Desktop application look and feel

2. **Toolbar**
   - Quick access buttons: New, Save, Load, Settings, Help
   - Icon-based interface

3. **Status Bar**
   - Current status message
   - Function name
   - Progress percentage
   - Mouse position tracking

4. **Window Controls**
   - Minimize, Maximize, Close buttons
   - Fullscreen toggle support

5. **Information Panel**
   - Current iteration number
   - Best fitness value (scientific notation)
   - PP (Predefined Probability) value
   - Convergence plot (mini chart)
   - Agent statistics

## File Structure

```
HW1/
├── gui_app/
│   ├── backend/
│   │   └── server.py              # Flask server with API endpoints
│   ├── frontend/
│   │   ├── templates/
│   │   │   └── index.html         # Main GUI page
│   │   └── static/
│   │       ├── css/
│   │       │   └── style.css      # GUI styling (598 lines)
│   │       └── js/
│   │           └── app.js         # Frontend logic (783 lines)
│   ├── requirements.txt           # Python dependencies
│   ├── README.md                  # Usage guide
│   ├── INSTALLATION.md            # Installation instructions
│   ├── run.sh                     # Startup script (Unix)
│   └── run.bat                    # Startup script (Windows)
├── ifraimova/
│   └── dolphin.py                 # Core algorithm from HW1
└── HW2_SUMMARY.md                 # This file
```

## Technical Implementation

### 2D Visualization Method

For an N-dimensional function:

1. User selects exactly 2 variables via checkboxes (e.g., x₀ and x₁)
2. Other variables are fixed using slider values (constants)
3. Function f(x₀, x₁, ..., xₙ) becomes f(x₀, x₁, c₂, ..., cₙ)
4. Backend evaluates function on a 50×50 grid
5. Frontend displays as interactive contour plot with Plotly.js

### Step-by-Step Execution

Each step performs:

1. Calculate predefined probability (PP) for current iteration
2. Calculate accumulative fitness for each agent
3. Update each agent's position using DEO algorithm
4. Evaluate fitness at new positions
5. Update best solution if improved
6. Send complete state to frontend via REST API
7. Frontend updates visualization immediately

### Real-Time Communication

- REST API for initialization and step execution
- WebSocket (Socket.IO) for future real-time streaming
- JSON data format for state transfer
- Efficient data serialization (only necessary fields)

## API Endpoints

- `GET /` - Serve main GUI page
- `GET /api/functions` - Get available test functions
- `POST /api/initialize` - Initialize optimization with parameters
- `POST /api/step` - Execute one iteration
- `POST /api/reset` - Reset optimization state
- `POST /api/evaluate_grid` - Get 2D function values for visualization

## Key Features

1. **Interactive Visualization**
   - Zoom, pan, and hover on plots
   - Mouse position shows coordinates
   - Color bar indicates function values
   - Responsive canvas resizing

2. **Dynamic Controls**
   - Sliders automatically generated based on dimension
   - Checkboxes for variable selection
   - Real-time synchronization between controls

3. **Progress Monitoring**
   - Iteration counter
   - Best fitness tracking
   - Convergence curve (log scale)
   - Progress percentage

4. **User-Friendly Interface**
   - Clear visual hierarchy
   - Intuitive button placement
   - Status messages for all actions
   - Help dialog with instructions

## Running the Application

### Quick Start:

```bash
cd gui_app
./run.sh  # On macOS/Linux
# or
run.bat   # On Windows
```

### Manual Start:

```bash
cd gui_app
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd backend
python server.py
```

Then open browser at: `http://localhost:5000`

## Usage Workflow

1. **Initialize**
   - Select function (Sphere/Rastrigin/Rosenbrock)
   - Set population size, iterations, dimension
   - Click "Initialize Optimization"

2. **Configure Visualization**
   - Select 2 variables with checkboxes
   - Adjust sliders for other variables
   - Plot updates automatically

3. **Run Optimization**
   - Click "Step" for single iteration
   - Click "Start" for continuous execution
   - Click "Stop" to pause
   - Watch agents move in real-time

4. **Monitor Progress**
   - View convergence curve
   - Check best fitness value
   - See agent positions and trajectories
   - Track iteration count

5. **Save Results**
   - Click "Save" button in toolbar
   - Downloads JSON file with results

## Testing

The application has been tested with:

- Multiple function types (Sphere, Rastrigin, Rosenbrock)
- Various dimensions (2-20)
- Different population sizes (5-100)
- Step-by-step and continuous execution modes
- Variable selection and slider interactions

## Dependencies

**Python (Backend):**

- flask >= 3.0.0
- flask-socketio >= 5.3.0
- flask-cors >= 4.0.0
- numpy >= 1.24.0
- python-socketio >= 5.10.0
- eventlet >= 0.33.0

**JavaScript (Frontend):**

- Socket.IO 4.5.4 (CDN)
- Plotly.js 2.27.0 (CDN)

## Browser Compatibility

Tested and working on:

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Evaluation Criteria Met

### Core (up to 6 points)

✅ Metaheuristic implemented according to HW1 requirements (mark 8+)
✅ GUI with canvas for 2D function visualization
✅ Function selection dropdown
✅ Sliders and textboxes for variables
✅ Checkbox selection (exactly 2 variables)
✅ Solution visualization on 2D plot

### Additional (up to 8 points)

✅ All grade 6 requirements
✅ Parameter panel (always visible, not dialog)
✅ Step-by-step visualization with Start/Step/Stop buttons
✅ Agent positions with numbers
✅ Best solution clearly marked (yellow star)
✅ Agent trajectories with toggle option

### Extra Features (Bonus)

✅ Menu bar and toolbar
✅ Status bar with real-time info
✅ Window controls
✅ Convergence plot
✅ Save/Load functionality
✅ Help system
✅ Responsive design
✅ Professional UI/UX

## Conclusion

This implementation provides a complete, professional-grade GUI application for the Dolphin Echolocation optimization algorithm. It meets all requirements for Track 2a, Grade 8, and includes additional features for enhanced usability and visualization.

The client-server architecture (Python backend + JavaScript frontend) provides:

- Clean separation of concerns
- Real-time visualization capabilities
- Cross-platform compatibility
- Professional desktop application experience
- Extensibility for future enhancements

**Grade Target: 8/10**

All mandatory requirements are fully implemented and tested.
