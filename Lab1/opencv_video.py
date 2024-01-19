import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Convert frame to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Define HSV threshold values for slightly darker blue color
    lower_hsv = np.array([90, 50, 20])
    upper_hsv = np.array([140, 255, 150])
    # Create HSV mask
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Define RGB threshold values for slightly darker blue color
    lower_rgb = np.array([5, 5, 95])
    upper_rgb = np.array([120, 120, 255])

    # Create RGB mask
    mask_rgb = cv2.inRange(rgb, lower_rgb, upper_rgb)

    # Find contours for HSV
    contours_hsv, _ = cv2.findContours(
        mask_hsv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour for HSV
    largest_contour_hsv = max(contours_hsv, key=cv2.contourArea, default=None)
    # Draw bounding box for the largest contour in HSV
    frame_hsv = frame.copy()
    if largest_contour_hsv is not None:
        x, y, w, h = cv2.boundingRect(largest_contour_hsv)
        cv2.rectangle(frame_hsv, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # # Draw bounding boxes for HSV
    # frame_hsv = frame.copy()
    # for contour in contours_hsv:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(frame_hsv, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Find contours for RGB
    contours_rgb, _ = cv2.findContours(
        mask_rgb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour for RGB
    largest_contour_rgb = max(contours_rgb, key=cv2.contourArea, default=None)

    # Draw bounding box for the largest contour in RGB
    frame_rgb = frame.copy()
    if largest_contour_rgb is not None:
        x, y, w, h = cv2.boundingRect(largest_contour_rgb)
        cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # # Draw bounding boxes for RGB
    # frame_rgb = frame.copy()
    # for contour in contours_rgb:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frames
    cv2.imshow('Bounding Boxes - HSV', frame_hsv)
    cv2.imshow('Bounding Boxes - RGB', frame_rgb)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
