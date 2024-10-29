import cv2
import os

directory = 'ControlImage48x48/'

# Ensure required directories exist
if not os.path.exists(directory):
    os.mkdir(directory)
if not os.path.exists(f'{directory}/blank'):
    os.mkdir(f'{directory}/blank')

for i in range(65, 71):
    letter = chr(i)
    if not os.path.exists(f'{directory}/{letter}'):
        os.mkdir(f'{directory}/{letter}')

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    cv2.namedWindow("data", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("data", 1280, 720)

    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame, (0, 40), (300, 300), (255, 255, 255), 2)
    # Create a transparent overlay
    overlay = frame.copy()

    # Get counts for each directory
    count = {
        'a': len(os.listdir(directory + "/A")) if os.path.exists(directory + "/A") else 0,
        'b': len(os.listdir(directory + "/B")) if os.path.exists(directory + "/B") else 0,
        'c': len(os.listdir(directory + "/C")) if os.path.exists(directory + "/C") else 0,
        'd': len(os.listdir(directory + "/D")) if os.path.exists(directory + "/D") else 0,
        'e': len(os.listdir(directory + "/E")) if os.path.exists(directory + "/E") else 0,
        'f': len(os.listdir(directory + "/F")) if os.path.exists(directory + "/F") else 0,
        'blank': len(os.listdir(directory + "/blank")) if os.path.exists(directory + "/blank") else 0
    }

    row = frame.shape[1]
    col = frame.shape[0]

    # Define positions for two-row display and reduce text size
    positions = [
        (10, col - 90), (220, col - 90), (430, col - 90),  # Row 1
        (10, col - 30),  (220, col - 30),  (430, col - 30),   # Row 2
        (10, col - 150)  # Row 3
    ]
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
              (0,255,255), (255,0,255), (100, 100, 100)]
    labels = ["Up", "Right", "Down", "Left", "Vol up", "Vol Down", "Blank"]

    # Display counts with transparent background
    for i, key in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'blank']):
        cv2.putText(overlay, f'{labels[i]}: {count[key]}', 
                    positions[i], cv2.FONT_HERSHEY_SIMPLEX, 0.8, colors[i], 2, cv2.LINE_AA)

    # Apply transparent overlay
    alpha = 1  # Transparency factor
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Display quit message
    cv2.putText(frame, 'Press "q" to quit', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("data", frame)

    # Extract the ROI
    roi = frame[40:300, 0:300]
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    roi_resized = cv2.resize(roi_gray, (48, 48))

    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == ord('a'):
        cv2.imwrite(os.path.join(directory + 'A/' + str(count['a'])) + '.jpg', roi_resized)
    if interrupt & 0xFF == ord('b'):
        cv2.imwrite(os.path.join(directory + 'B/' + str(count['b'])) + '.jpg', roi_resized)
    if interrupt & 0xFF == ord('c'):
        cv2.imwrite(os.path.join(directory + 'C/' + str(count['c'])) + '.jpg', roi_resized)
    if interrupt & 0xFF == ord('d'):
        cv2.imwrite(os.path.join(directory + 'D/' + str(count['d'])) + '.jpg', roi_resized)
    if interrupt & 0xFF == ord('e'):
        cv2.imwrite(os.path.join(directory + 'E/' + str(count['e'])) + '.jpg', roi_resized)
    if interrupt & 0xFF == ord('f'):
        cv2.imwrite(os.path.join(directory + 'F/' + str(count['f'])) + '.jpg', roi_resized)
    if interrupt & 0xFF == ord('.'):
        cv2.imwrite(os.path.join(directory + 'blank/' + str(count['blank'])) + '.jpg', roi_resized)
    if interrupt & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
