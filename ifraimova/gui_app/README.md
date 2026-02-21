# Dolphin Echolocation Optimization - GUI Application

A comprehensive desktop GUI application for visualizing and controlling the Dolphin Echolocation metaheuristic optimization algorithm.

## Features

### Core Requirements (Grade 8)

✅ **Metaheuristic Implementation**: Full Dolphin Echolocation Algorithm from HW1
✅ **GUI Components**:

- Menu bar (File, Edit, View, Help)
- Toolbar with action buttons
- Status bar with real-time information
- Window controls (minimize, maximize, close)

✅ **2D Function Visualization**:

- Interactive canvas with 2D contour plots
- Dynamic function selection (Sphere, Rastrigin, Rosenbrock)
- Sliders for each variable dimension
- Text boxes synchronized with sliders
- Checkbox selection for 2 variables to visualize
- Color bar showing function value gradient
- Mouse position tracking with function value display

✅ **Algorithm Parameters Panel**:

- Population size (number of agents)
- Maximum iterations
- Function dimension
- All parameters visible and editable

✅ **Step-by-Step Execution**:

- **Start** button: Runs optimization continuously
- **Step** button: Executes one iteration at a time
- **Stop** button: Pauses execution
- Real-time visualization of:
  - Agent positions (numbered points)
  - Best solution (yellow star)
  - Agent trajectories (dashed lines, toggleable)

✅ **Real-time Information Display**:

- Current iteration number
- Best fitness value
- Best solution coordinates
- Convergence plot
- Agent statistics
- Progress percentage

## Architecture

### Backend (Python)

- **Framework**: Flask with Flask-SocketIO
- **Algorithm**: Extended DolphinEcholocation class with step-by-step execution
- **API Endpoints**:
  - `/api/functions` - Get available test functions
  - `/api/initialize` - Initialize optimization
  - `/api/step` - Execute one iteration
  - `/api/reset` - Reset optimization
  - `/api/evaluate_grid` - Get 2D function values for visualization

### Frontend (JavaScript)

- **Visualization**: Plotly.js for interactive 2D plots
- **Communication**: Socket.IO for real-time updates
- **UI**: Responsive design with desktop application look

## Installation

1. Install Python dependencies:

```bash
cd gui_app
pip install -r requirements.txt
```

2. Ensure the dolphin.py module is accessible:

```bash
# The server.py automatically adds the ifraimova directory to the path
```

## Running the Application

1. Start the server:

```bash
cd gui_app/backend
python server.py
```

2. Open your browser and navigate to:

```
http://localhost:5000
```

## Usage Guide

### 1. Initialize Optimization

1. Select a test function (Sphere, Rastrigin, or Rosenbrock)
2. Set algorithm parameters:
   - Population Size: Number of agents (dolphins)
   - Max Iterations: Maximum number of iterations
   - Dimension: Number of variables
3. Click **"Initialize Optimization"**

### 2. Configure Visualization

1. Select exactly 2 variables using checkboxes (for 2D visualization)
2. Use sliders to set values for other variables (fixed constants)
3. The plot updates automatically showing the function landscape

### 3. Run Optimization

- **Step**: Execute one iteration and see agents move
- **Start**: Run continuously until completion or stopped
- **Stop**: Pause execution at any time
- **Reset**: Clear everything and start over

### 4. Monitor Progress

- Watch agents (white circles with numbers) move on the plot
- See the best solution (yellow star) update in real-time
- View convergence curve in the right panel
- Track iteration count and best fitness value

### 5. Visualization Options

- ☑ **Show Agent Trajectories**: Display dashed lines showing agent paths
- ☑ **Show Best Solution**: Display the best solution as a star

## File Structure

```
gui_app/
├── backend/
│   └── server.py           # Flask server with API endpoints
├── frontend/
│   ├── templates/
│   │   └── index.html      # Main GUI page
│   └── static/
│       ├── css/
│       │   └── style.css   # GUI styling
│       └── js/
│           └── app.js      # Frontend logic
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Technical Details

### 2D Visualization Method

When visualizing an N-dimensional function in 2D:

1. User selects 2 variables (e.g., x₀ and x₁) via checkboxes
2. Other variables are fixed using slider values
3. The function f(x₀, x₁, ..., xₙ) becomes f(x₀, x₁, c₂, ..., cₙ)
4. A 2D grid is evaluated and displayed as a contour plot

### Agent Visualization

- **Agents**: White circles with black borders, numbered 0 to N-1
- **Best Solution**: Yellow star with black border
- **Trajectories**: Dashed white lines connecting previous positions
- **Color Map**: Blue (low values) → Red (high values)

### Step-by-Step Execution

Each step performs:

1. Calculate predefined probability (PP)
2. Calculate accumulative fitness for each agent
3. Update each agent's position
4. Evaluate fitness at new positions
5. Update best solution if improved
6. Send state to frontend for visualization

## Requirements Met

### Track 2a (Grade 6)

✅ Core metaheuristic implementation
✅ GUI with canvas for 2D visualization
✅ Function selection dropdown
✅ Sliders for variable control
✅ Checkboxes for variable selection
✅ Solution visualization on plot

### Track 2a (Grade 8)

✅ All grade 6 requirements
✅ Parameter configuration panel (always visible)
✅ Step-by-step visualization with Start/Step/Stop buttons
✅ Agent positions displayed with numbers
✅ Best solution marked distinctly
✅ Agent trajectories with toggle option
✅ Real-time updates during execution

## Browser Compatibility

Tested on:

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Notes

- The application uses WebSocket for real-time communication
- All computations are performed on the server (Python backend)
- The frontend handles only visualization and user interaction
- Function evaluation is done server-side for accuracy

## Troubleshooting

**Port already in use:**

```bash
# Change port in server.py line 349:
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

**Module not found error:**

```bash
# Ensure you're running from the correct directory
cd gui_app/backend
python server.py
```

**Visualization not updating:**

- Check browser console for errors
- Ensure WebSocket connection is established
- Try refreshing the page

## License

This application is part of the HW2 assignment for the optimization course.
