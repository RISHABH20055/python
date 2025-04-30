# Import required libraries
import cv2
import numpy as np
import HandTrackingModule as htm  # Custom module for hand detection
import autopy  # For controlling mouse cursor
import time

########################
wCam, hCam = 640, 480  # Webcam resolution
frameR = 100  # Margin from screen edges to avoid abrupt movement
smoothening = 7  # Smooth cursor movement
########################

# Initialize previous and current location of cursor
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Open the webcam
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize hand detector with 1 hand max
detector = htm.handDetector(maxHands=1)

# Get screen width and height
wScr, hScr = autopy.screen.size()

# Function to check which fingers are up
def fingersUp(lmList):
    fingers = []
    tipIds = [4, 8, 12, 16, 20]

    # Thumb (checks if it's to the right of its base)
    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers (check if fingertip is above middle joint)
    for id in range(1, 5):
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

# Main loop
while True:
    success, img = cap.read()  # Read frame from webcam
    img = detector.findHands(img)  # Detect hands and draw landmarks
    lmList = detector.findPosition(img, draw=False)  # Get landmark positions

    if len(lmList) != 0:
        # Get tip positions of index and middle fingers
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip

        fingers = fingersUp(lmList)  # Which fingers are up?

        if fingers[1] == 1 and fingers[2] == 0:
            # Moving mode: Only index finger up
            # Convert webcam coordinates to screen coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # Smooth the cursor movement
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Move the mouse
            autopy.mouse.move(wScr - clocX, clocY)
            plocX, plocY = clocX, clocY  # Update previous position

            # Draw a circle on the index finger
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

        if fingers[1] == 1 and fingers[2] == 1:
            # Click mode: Index and middle fingers both up
            length = np.hypot(x2 - x1, y2 - y1)  # Distance between tips
            if length < 40:  # If fingers are close, do a click
                cv2.circle(img, ((x1 + x2) // 2, (y1 + y2) // 2),
                           10, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime + 1e-5)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show the webcam feed
    cv2.imshow("Virtual Mouse", img)

    # Break loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
