from tensorflow.keras.models import model_from_json
import cv2
import numpy as np
import time
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load the model
json_file = open("model/signdetectioncontrolmodel48x48.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("model/signdetectioncontrolmodel48x48.h5")

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

# Initialize audio endpoint volume control using pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def get_volume():
    """Get the current system volume."""
    return int(volume.GetMasterVolumeLevelScalar() * 100)

def change_volume(volume_up):
    """Increase or decrease volume. True for up, False for down."""
    step = 0.02 if volume_up else -0.02
    new_volume = max(0, min(1, volume.GetMasterVolumeLevelScalar() + step))
    volume.SetMasterVolumeLevelScalar(new_volume, None)

# Initialize video capture
cap = cv2.VideoCapture(0)
label = ['A', 'B', 'C', 'D', 'E', 'F', 'blank']
dis = {'A': 'Up', 'B': 'Right', 'C': 'Down', 'D': 'Left', 'E': 'Vol Up', 'F': 'Vol Down', 'blank': 'blank'}

# Variables for calculating FPS
prev_frame_time = 0
new_frame_time = 0

# Set the window size
window_name = 'Sign Language Detection'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1000, 800)  # Resize the window to 1000x800 pixels

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    # Calculate FPS
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    # Define the region of interest
    cv2.rectangle(frame, (0, 40), (300, 300), (0, 165, 255), 2)
    roi = frame[40:300, 0:300]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (48, 48))
    features = extract_features(resized)

    # Make prediction
    pred = model.predict(features)
    prediction_label = label[pred.argmax()]

    # Perform actions based on the prediction
    if prediction_label == 'A':  # Move mouse up
        pyautogui.move(0, -20)
    elif prediction_label == 'B':  # Move mouse right
        pyautogui.move(20, 0)
    elif prediction_label == 'C':  # Move mouse down
        pyautogui.move(0, 20)
    elif prediction_label == 'D':  # Move mouse left
        pyautogui.move(-20, 0)
    elif prediction_label == 'E':  # Volume up
        change_volume(True)
    elif prediction_label == 'F':  # Volume down
        change_volume(False)

    # Get current mouse position and volume
    mouse_x, mouse_y = pyautogui.position()
    current_volume = get_volume()

    # Display the results
    cv2.rectangle(frame, (0, 0), (1000, 40), (50, 50, 50), -1)  # Darker background for contrast
    cv2.putText(frame, "Prediction:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    if prediction_label == 'blank':
        cv2.putText(frame, "Empty", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        accuracy = "{:.2f}".format(np.max(pred) * 100)
        cv2.putText(frame, f'{dis[prediction_label]} ({accuracy}%)', (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display FPS
    cv2.putText(frame, f'FPS: {int(fps)}', (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display mouse position and volume (adjusting font size and positions)
    cv2.putText(frame, f'Mouse Position: ({mouse_x}, {mouse_y})', (10, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f'Volume: {current_volume}%', (10, 720), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

    # Display the frame
    cv2.imshow(window_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
