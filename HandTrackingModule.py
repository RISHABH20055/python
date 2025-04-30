# Import OpenCV for image processing and MediaPipe for hand tracking
import cv2
import mediapipe as mp

# Define a class for hand detection
class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # Initialize parameters
        self.mode = mode  # Static image mode or video stream
        self.maxHands = maxHands  # Maximum number of hands to detect
        self.detectionCon = detectionCon  # Minimum detection confidence
        self.trackCon = trackCon  # Minimum tracking confidence

        # Load MediaPipe's hands module
        self.mpHands = mp.solutions.hands

        # Create a Hands object with the specified settings
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        # Load the drawing utility to draw hand landmarks
        self.mpDraw = mp.solutions.drawing_utils

        # List of landmark IDs for fingertips
        self.tipIds = [4, 8, 12, 16, 20]

    # Method to detect hands and optionally draw landmarks
    def findHands(self, img, draw=True):
        # Convert the image from BGR to RGB (MediaPipe uses RGB)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the image to detect hands
        self.results = self.hands.process(imgRGB)

        # Check if hands are detected
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw the landmarks and connections on the image
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        # Return the image (with or without drawings)
        return img

    # Method to find and return the positions of landmarks in one hand
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []  # List to store landmark positions

        # Check if hands were detected
        if self.results.multi_hand_landmarks:
            # Select the specific hand (default is the first one)
            myHand = self.results.multi_hand_landmarks[handNo]

            # Loop through each landmark in the selected hand
            for id, lm in enumerate(myHand.landmark):
                # Get image dimensions
                h, w, _ = img.shape

                # Convert normalized coordinates to pixel values
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Add the landmark ID and position to the list
                lmList.append((id, cx, cy))

                # Optionally draw a circle at each landmark point
                if draw:
                    cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

        # Return the list of landmark positions
        return lmList
