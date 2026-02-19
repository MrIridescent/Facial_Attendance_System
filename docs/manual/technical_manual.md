# Facial Attendance System: Simplified Technical Manual
### Version 2.0 - The Renaissance Edition

## 1. Introduction
The **Facial Attendance System** is a professional-grade automated tool designed for high-accuracy identity verification and timestamped logging. This manual provides a step-by-step guide for installation, configuration, and operation.

## 2. Hardware & Environment Recommendations
To ensure 10x performance and production-readiness, the following specifications are recommended:

- **Processor**: Intel Core i5/i7 (8th Gen+) or AMD Ryzen 5/7 for smooth real-time recognition.
- **RAM**: Minimum 8GB (16GB recommended for large datasets).
- **Graphics (Optional)**: NVIDIA GPU with CUDA support for accelerated dlib processing.
- **Camera**: 720p or 1080p high-quality USB/Integrated webcam.
- **Operating System**: Windows 10/11, Ubuntu 20.04+, or macOS.

## 3. Turnkey Installation (The Wizard Way)
We have automated the complex installation process into a single command.

1.  **Clone the repository** to your local machine.
2.  **Open a terminal/command prompt** in the project root.
3.  **Run the Wizard**:
    ```bash
    python setup_wizard.py
    ```
    *The wizard will detect your environment, install CMake, dlib (via wheels or source), and all other dependencies automatically.*

## 4. Manual Configuration (The Expert Way)
If you prefer manual setup:
1.  **Install dependencies**:
    `pip install face_recognition opencv-python numpy cmake`
2.  **Verify dlib**: If `pip install dlib` fails, use one of the provided `.whl` files in the root directory.

## 5. Daily Operation
### Step A: Preparing Known Faces
- Place clear, front-facing images of individuals in `src/data/known_faces/`.
- Name files as you want them to appear (e.g., `Mriridescent_based.png`).
- Supported formats: `.png`, `.jpg`, `.jpeg`.

### Step B: Starting the Engine
- Run the main script:
  ```bash
  python src/main.py
  ```
- A window titled **"Facial Attendance System - S_STAR S.B"** will appear.
- Recognized faces will be highlighted with a red box and their name.

### Step C: Stopping and Logging
- Press **'q'** on your keyboard to safely shutdown the engine.
- Attendance logs are automatically saved in `src/data/logs/` in a CSV format named by the current date (e.g., `2026-02-19.csv`).

## 6. Troubleshooting & Best Practices
- **Lighting**: Ensure the subject's face is well-lit from the front.
- **Angle**: The camera should be at eye level for best recognition results.
- **Background**: A neutral background reduces processing noise.
- **Multiple Faces**: The system supports multiple simultaneous detections.

---
**Mriridescent based**
*Digital Polymath & Renaissance Architect*
