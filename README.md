To run your Virtual Mouse Project, you need to install several Python libraries. Here's a list of the dependencies and the corresponding commands to install them.
 # ( starting with # are the commands for dependencies to run in terminal )
✅ 1. Install Required Dependencies
🔹 1. OpenCV (for image processing)

 # pip install opencv-python

 
🔹 2. NumPy (for numerical operations)

# pip install numpy


🔹 3. autopy (for controlling mouse and screen)

# pip install autopy


⚠️ Note: On Windows, you might face issues installing autopy. If it fails, use:


# pip install git+https://github.com/autopilot-rs/autopy.git


🔹 4. MediaPipe (for hand detection, used in your HandTrackingModule)

# pip install mediapipe


🔹 5. Custom HandTrackingModule.py
Make sure your project folder contains the HandTrackingModule.py file that wraps MediaPipe's hand tracking functionality.

If you don’t have it, I can help you create one.

✅ 2. Optional (for performance monitoring)

# pip install time


⚠️ You don’t need to install time separately. It is a built-in Python module.

📦 Install All at Once (Recommended)
You can use this one-liner to install everything:


# pip install opencv-python numpy autopy mediapipe
