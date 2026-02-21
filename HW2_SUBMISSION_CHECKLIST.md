# HW2 Submission Checklist

## 📋 LMS Upload Requirements

### ✅ Required Files Created

1. **ifraimova_hw2.txt** ✓
   - Location: `/Users/mayaffia/Desktop/HW1/ifraimova_hw2.txt`
   - Contains: Track 2a, Target grade 8, Applications info

2. **ifraimova_hw2_youtube.txt** ✓
   - Location: `/Users/mayaffia/Desktop/HW1/ifraimova_hw2_youtube.txt`
   - Status: ⚠️ NEEDS VIDEO LINK - Please record and add your YouTube/RuTube link

### 📁 Folder Structure

```
HW1/
├── ifraimova/                    ✓ (main submission folder)
│   ├── dolphin.py               (your algorithm implementation)
│   ├── demo_2d_visualization.py
│   ├── run_with_data.py
│   ├── test_examples.py
│   ├── visualization_2d.py
│   ├── requirements.txt
│   └── gui_app/                 ✓ (GUI application for HW2)
│       ├── backend/
│       │   └── server.py
│       ├── react-frontend/
│       │   ├── src/
│       │   │   ├── App.js
│       │   │   ├── App.css
│       │   │   ├── index.js
│       │   │   └── index.css
│       │   ├── public/
│       │   │   └── index.html
│       │   └── package.json
│       ├── requirements.txt
│       ├── README.md
│       ├── FINAL_README.md
│       ├── INSTALLATION.md
│       ├── START.md
│       ├── run.sh
│       └── run.bat
│
├── resourses/                    ✓ (resources folder)
│   ├── Dolphin_Echolocation (1).pdf
│   └── resourses.txt
│
├── iodata/                       ✓ (input/output data)
│   ├── input_data.json
│   ├── results_*.txt
│   ├── *.png (visualization images)
│   └── deo_animation.gif
│
├── ifraimova_hw2.txt            ✓
├── ifraimova_hw2_youtube.txt    ⚠️ (needs video link)
├── HW2_SUMMARY.md               ✓
└── paper.pdf                     ✓ (Dolphin Echolocation paper)
```

## 🎥 Video Recording Requirements

### Must Include in 7-Minute Demo:

1. **Code Structure (1-2 min)**
   - Show `gui_app/` folder structure
   - Explain backend (`server.py`) and frontend (`react-frontend/`)
   - Mention Dolphin algorithm from `ifraimova/dolphin.py`

2. **GUI Overview (1 min)**
   - Show the main interface
   - Point out: canvas, parameter panel, controls, status bar
   - Highlight menu bar and toolbar

3. **Configuration & Running (1 min)**
   - Show how to start the application:
     ```bash
     cd ifraimova/gui_app
     ./run.sh  # or run.bat on Windows
     ```
   - Or manual start with backend + frontend

4. **Usage Scenarios (2-3 min)**
   - Select a function (Sphere/Rastrigin/Rosenbrock)
   - Set parameters (population size, iterations, dimension)
   - Click "Initialize Optimization"
   - Select 2 variables with checkboxes
   - Adjust sliders for other variables
   - Show how plot updates

5. **Step-by-Step Mode (1-2 min)** ⭐ IMPORTANT
   - Click "Step" button - show one iteration
   - Click "Step" again - show next iteration
   - Click "Start" - show continuous execution
   - Click "Stop" - pause execution
   - Show agent positions updating
   - Show trajectories (toggle on/off)
   - Show best solution (yellow star)

6. **Proof of Requirements (30 sec)**
   - Show agent numbers on plot
   - Show trajectories with dashed lines
   - Show parameter panel (always visible)
   - Show convergence plot
   - Show best fitness value

## ✅ Evaluation Criteria Verification

### Track 2a - Grade 6 (Base Requirements)

- ✅ Metaheuristic from HW1 (grade 8+)
- ✅ GUI with canvas for 2D visualization
- ✅ Function selection dropdown
- ✅ Sliders and textboxes for variables
- ✅ Checkbox selection (exactly 2 variables)
- ✅ Solution visualization on 2D plot

### Track 2a - Grade 8 (Additional Requirements)

- ✅ Parameter panel (always visible, not dialog)
- ✅ Step-by-step visualization (Start/Step/Stop buttons)
- ✅ Agent positions with numbers
- ✅ Best solution clearly marked (yellow star)
- ✅ Agent trajectories with toggle option

## 📝 Papers Required

1. **Dolphin Echolocation Paper** ✓
   - Location: `resourses/Dolphin_Echolocation (1).pdf`
   - This is the metaheuristic paper

2. **Application Paper** (if targeting grade 10)
   - Not applicable - targeting grade 8

## 🚀 Quick Test Before Recording

Run these commands to verify everything works:

```bash
# Terminal 1 - Backend
cd ifraimova/gui_app
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cd backend
python server.py

# Terminal 2 - Frontend
cd ifraimova/gui_app/react-frontend
npm install
npm start
```

Then test:

1. Open http://localhost:3000
2. Select "Sphere" function
3. Set: Population=20, Iterations=50, Dimension=3
4. Click "Initialize Optimization"
5. Select checkboxes for x₀ and x₁
6. Click "Step" several times
7. Click "Start" to run continuously
8. Click "Stop" to pause
9. Toggle "Show Trajectories"
10. Verify agents move and best solution updates

## 📤 Final Submission Steps

1. ⚠️ **RECORD VIDEO** - 7 minutes maximum
2. ⚠️ **UPLOAD VIDEO** to YouTube/RuTube
3. ⚠️ **UPDATE** `ifraimova_hw2_youtube.txt` with video link
4. ✅ Verify all files in checklist exist
5. ✅ Create ZIP archive or prepare folder for upload
6. ✅ Submit to LMS

## 📦 What to Submit

Create a folder named **"ifraimova"** containing:

```
ifraimova/
├── dolphin.py                    (your algorithm)
├── demo_2d_visualization.py
├── run_with_data.py
├── test_examples.py
├── visualization_2d.py
├── requirements.txt
└── (other source files)
```

Plus at the root level:

- `ifraimova_hw2.txt`
- `ifraimova_hw2_youtube.txt` (with video link!)
- `resourses/` folder
- `iodata/` folder
- `gui_app/` folder (entire GUI application)
- `paper.pdf` (Dolphin Echolocation paper)

## ⚠️ CRITICAL REMINDERS

1. **Video must be exactly 7 minutes or less** (firm requirement)
2. **Must demonstrate step-by-step mode** clearly
3. **Must show GUI works** as required
4. **Must prove evaluation criteria** are met
5. **Video link must be added** to `ifraimova_hw2_youtube.txt`

## 🎬 Video Recording Tips

- Use screen recording software (OBS, QuickTime, etc.)
- Show your face (optional but recommended)
- Speak clearly and explain what you're doing
- Practice once before final recording
- Keep it under 7 minutes!
- Show the GUI in action, not just code

## ✨ Current Status

- ✅ GUI Application: COMPLETE
- ✅ Documentation: COMPLETE
- ✅ Source Code: COMPLETE
- ✅ Test Data: COMPLETE
- ⚠️ Video: NEEDS TO BE RECORDED
- ⚠️ Video Link: NEEDS TO BE ADDED

**Next Step: Record your 7-minute demonstration video!**
