import os
import sys
import subprocess
import shutil
import platform

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def run_command(command, description):
    print(f"\n[+] {description}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + command.split())
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error: {str(e)}")
        return False

def wizard():
    clear_screen()
    print("====================================================")
    print("   FACIAL ATTENDANCE SYSTEM - TURNKEY SETUP WIZARD   ")
    print("        Created by: Mriridescent based           ")
    print("====================================================")
    
    # 1. Check Python version
    print(f"\n[i] Detecting Environment...")
    print(f"    Python Version: {platform.python_version()}")
    print(f"    Platform: {platform.system()} {platform.release()}")

    # 2. Project Directory Setup
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "src/data/known_faces")
    logs_dir = os.path.join(base_dir, "src/data/logs")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"[+] Created data directory: {data_dir}")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"[+] Created logs directory: {logs_dir}")

    # 3. Dependency Installation
    print("\n[i] Installing Core Dependencies...")
    
    # Install cmake first (often needed for dlib)
    run_command("cmake", "Installing CMake")
    
    # Try installing dlib (if on windows, might need wheel)
    if platform.system() == "Windows":
        py_version = platform.python_version_tuple()
        if py_version[0] == '3' and py_version[1] == '11':
            wheel_path = "dlib-19.24.1-cp311-cp311-win_amd64.whl"
            if os.path.exists(wheel_path):
                print(f"[+] Found local dlib wheel for Python 3.11: {wheel_path}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", wheel_path])
        elif py_version[0] == '3' and py_version[1] == '9':
            wheel_path = "dlib-19.22.1-cp39-cp39-win_amd64.whl"
            if os.path.exists(wheel_path):
                print(f"[+] Found local dlib wheel for Python 3.9: {wheel_path}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", wheel_path])

    # Install the rest
    dependencies = ["face_recognition", "opencv-python", "numpy", "logging"]
    for dep in dependencies:
        run_command(dep, f"Installing {dep}")

    print("\n====================================================")
    print("   SETUP COMPLETE! YOUR SYSTEM IS READY TO USE!    ")
    print("====================================================")
    print("\nNext Steps:")
    print(f"1. Place images of known people in: {data_dir}")
    print("2. Run the system using: python src/main.py")
    print("3. Attendance logs will appear in: src/data/logs")
    print("\nEnjoy the Renaissance of Attendance Automation!")

if __name__ == "__main__":
    wizard()
