# based on https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist


def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    return bar


# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Initialize KMeans clustering with 3 clusters
clt = KMeans(n_clusters=3, n_init=10)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Define the rectangle in the center of the screen
    rect_start_x = int(width * 0.25)
    rect_end_x = int(width * 0.75)
    rect_start_y = int(height * 0.25)
    rect_end_y = int(height * 0.75)

    # Crop the frame to the defined rectangle
    frame_cropped = frame[rect_start_y:rect_end_y, rect_start_x:rect_end_x]

    # Convert cropped frame to RGB
    frame_rgb = cv2.cvtColor(frame_cropped, cv2.COLOR_BGR2RGB)

    # Reshape the frame
    img = frame_rgb.reshape((frame_rgb.shape[0] * frame_rgb.shape[1], 3))

    # Perform KMeans clustering
    clt.fit(img)

    # Calculate histogram
    hist = find_histogram(clt)

    # Plot and display the dominant colors
    bar = plot_colors2(hist, clt.cluster_centers_)
    plt.axis("off")
    plt.imshow(bar)
    plt.pause(0.1)  # Pause for a short time to update the plot
    plt.clf()       # Clear the previous plot

# Release the capture object
cap.release()
