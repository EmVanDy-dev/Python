import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands object with optimizations
hands = mphands.Hands(
    max_num_hands=2,  # Detect up to 2 hands
    model_complexity=0,  # Use the lightest model for faster processing
    min_detection_confidence=0.5,  # Lower confidence threshold for faster detection
    min_tracking_confidence=0.5  # Lower tracking confidence for smoother performance
)

# Frame skipping and resolution settings
skip_frames = 2  # Process every 2nd frame
frame_counter = 0
resize_width = 640  # Resize frame width for faster processing

while True:
    # Read a frame from the camera
    ret, image = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Increment frame counter
    frame_counter += 1

    # Skip frames to reduce processing load
    if frame_counter % skip_frames != 0:
        continue

    # Resize the frame to a smaller resolution
    image = cv2.resize(image, (resize_width, int(image.shape[0] * (resize_width / image.shape[1]))))

    # Flip the image horizontally and convert the color space to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process the image to detect hand landmarks
    results = hands.process(image)

    # Convert the image back to BGR for display
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Initialize total finger count
    total_fingers = 0

    if results.multi_hand_landmarks:
        for i, (hand_landmarks, handedness) in enumerate(zip(results.multi_hand_landmarks, results.multi_handedness)):
            # Draw landmarks on the image
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mphands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            # Get landmark positions
            landmarks = hand_landmarks.landmark

            # Determine handedness (left or right)
            hand_label = handedness.classification[0].label  # 'Left' or 'Right'

            # Check if fingers are extended
            fingers = [
                landmarks[mphands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mphands.HandLandmark.INDEX_FINGER_PIP].y,  # Index finger
                landmarks[mphands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[mphands.HandLandmark.MIDDLE_FINGER_PIP].y,  # Middle finger
                landmarks[mphands.HandLandmark.RING_FINGER_TIP].y < landmarks[mphands.HandLandmark.RING_FINGER_PIP].y,  # Ring finger
                landmarks[mphands.HandLandmark.PINKY_TIP].y < landmarks[mphands.HandLandmark.PINKY_PIP].y,  # Pinky finger
            ]

            # Thumb logic depends on handedness
            if hand_label == "Right":
                # For right hand, thumb is extended if THUMB_TIP.x < THUMB_IP.x
                fingers.append(landmarks[mphands.HandLandmark.THUMB_TIP].x < landmarks[mphands.HandLandmark.THUMB_IP].x)
            else:
                # For left hand, thumb is extended if THUMB_TIP.x > THUMB_IP.x
                fingers.append(landmarks[mphands.HandLandmark.THUMB_TIP].x > landmarks[mphands.HandLandmark.THUMB_IP].x)

            # Count the number of extended fingers for this hand
            finger_count = fingers.count(True)
            total_fingers += finger_count  # Add to the total finger count

            # Display handedness and finger count for this hand
            text_position = (10, 50 + i * 50)  # Adjust text position for each hand
            cv2.putText(image, f"Hand {i + 1}: {hand_label}, Fingers: {finger_count}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the total number of fingers
    cv2.putText(image, f"Total Fingers: {total_fingers}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the image
    cv2.imshow("Hand Tracker", image)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()