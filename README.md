# 2D MazeRunner User Manual

## Introduction
The MazeRunner simulation is a program that demonstrates artificial intelligence through evolutionary algorithms. The software trains virtual agents to navigate through mazes using neural networks that evolve and become smarter over generations. Users can observe how AI agents learn to find efficient paths from the start to the end goal positions throughout different maze configurations.

This manual assumes that you have a basic understanding that MazeRunner is a simulation tool for watching AI learn maze navigation, but does not assume familiarity with the specific controls, features, or evolutionary concepts that are involved.

---

## System Requirements

### For Source Code Installation
- **Operating System:** Windows 8 or later, macOS 10.15 or later, GNU/Linux  
- **Python:** Versions 3.8–3.14 are currently supported  
- **RAM:** At least 2 GB  
- **Disk Space:** 50 MB free space  
- **Display:** Minimum resolution of 1280x720 pixels  

### For Executable (.exe) Version
- **Operating System:** Windows 8 or later, macOS 10.15 or later, GNU/Linux  
- **RAM:** At least 2 GB  
- **Disk Space:** 100 MB free space  
- **Display:** Minimum resolution of 1280x720 pixels  
- **No additional software installation required**

---

## Installation Instructions

### Option 1: Installing from Source Code

1. **Install Python**  
   Download and install Python 3.8 or higher from the official website: https://python.org  
   Make sure to check the option to add Python to your PATH.

2. **Install Required Libraries**
   ```bash
   pip install pygame
   pip install numpy
   ```

3. **Download the Source Code**
   - Download the MazeRunner source code files to a folder on your computer  
   - Make sure all files from the repository are present, including the `src` folder and configuration files  

4. **Run the Program**
   ```bash
   python main.py
   ```

---

### Option 2: Installing the Executable Version

1. **Download the Executable:**
   - Obtain the MazeRunner executable package from the project repository.
2. **Extract the Files:**
   - Right-click the downloaded `.zip` folder
   - Select **"Extract All"**
   - Choose a destination folder
   - Ensure that all the files remain in the same folder as `MazeRunner.exe`

3. **Run the Program**:
   - Open the extracted folder
   - Double-Click `MazeRunner.exe`

---

## GitHub Release (Version 1.0)
Download the official release here:
- **MazeRunner v1.0**
  https://github.com/msnyd/Capstone_MazeRunner/releases/tag/v1.0

---

## Getting Started

When you first launch MazeRunner, you will see the main menu screen with three options:

- **Start Simulation** – Begins the maze navigation simulation  
- **Settings** – Allows you to modify simulation parameters  
- **Quit** – Exits the program  

Click **Start Simulation** to begin watching the AI agents learn.

---

## Using the Software

### Main Simulation Screen

Once the simulation starts, you will see:

- A maze layout with:
  - Black walls  
  - Open area (dark grey)  
  - Starting position (green)  
  - Goal position (red)  

- Multiple colored dots representing AI agents moving through the maze  

- An information panel (top left) showing:
  - Current generation  
  - Best fitness score  
  - Simulation statistics  

---

### Controls

Use the following keyboard controls during the simulation:

- `SPACE` – Pause or resume the simulation  
- `R` – Reset the current generation (agents return to start)  
- `N` – Force evolution to the next generation immediately  
- `F` – Toggle fast-forward mode (speeds up simulation)  
- `+` or `-` – Increase or decrease simulation speed  
- `ESC` – Return to the main menu  

---

### Interacting with Agents

- **Mouse Click** – Click on any agent (colored dot) to view its neural network structure and current inputs/outputs  
- `B` or `ESC` (in popup) – Close the neural network visualization popup  

---

### Settings Screen

Access settings from the main menu to modify:

- Population size (number of agents)  
- Maximum steps per generation  
- Neural network architecture  
- Genetic algorithm parameters (mutation rate, elite count)  
- Maze difficulty level  

Changes take effect when you start a new simulation.

---

## Features

### Maze Navigation Simulation
Agents use raycasting sensors to detect walls and the goal direction, feeding this information into neural networks that control their movement.

### Evolutionary Learning
Over generations, agents with better maze-solving abilities produce offspring with improved neural networks through genetic algorithms.

### Real-time Visualization
Watch agents learn in real-time, with options to speed up or slow down the simulation.

### Neural Network Inspection
Click any agent to see its current neural network structure, weights, and activation values.

### Multiple Difficulty Levels
Choose from:
- Easy  
- Medium  
- Hard  
- Very Hard  

---

## Troubleshooting

### Program Won’t Start

**Source Version:**
- Make sure Python is installed and added to PATH  
- Verify `pygame` and `numpy` are installed using:
  ```bash
  pip list
  ```

**Executable Version:**
- Ensure you are running a compatible operating system  
- Try running the program as administrator  
- Check that all required files are present  

---

### Simulation Runs Slowly

- Reduce the population size in settings  
- Enable fast mode using the `F` key  
- Close other programs to free up system resources  

---

### Agents Don’t Move or Learn

- Check that the simulation is not paused (`SPACE`)  
- Reset the generation with `R`
- If agents get stuck on a corner for too long, force evolving via `E` will force new paths  
- Verify maze files exist and are valid JSON format  

---

## Known Issues

- Large population sizes (>100) may cause performance issues on lower-end hardware  
- The executable version may trigger antivirus false positives (this is normal for bundled Python applications)  

---

## Support

For additional help or to report bugs:
- Contact the development team  
- Check the project repository for updates  

---

**Version:** 1.0  
Features and controls may vary in future versions.
