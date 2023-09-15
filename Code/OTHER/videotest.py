import cv2

# Open the video file
cap = cv2.VideoCapture('testvideo.mp4')

# Check if the video file was successfully opened
if not cap.isOpened():
    print("Error opening video file")

# Set the size of the video player window
cv2.namedWindow('Video Player', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video Player', 700, 500)

# Loop through the video frames
while cap.isOpened():
    # Read the next frame
    ret, frame = cap.read()

    # If the frame was successfully read, display it
    if ret:
        # Resize the frame to 700x700 pixels
        frame = cv2.resize(frame, (700, 500))
        cv2.imshow('Video Player', frame)

        # Wait for 25ms before showing the next frame
        key = cv2.waitKey(25)

        # If the space bar is pressed, skip the video
        if key == ord(' '):
            break
    else:
        # If there are no more frames, exit the loop
        break

# Release the video file and close the window
cap.release()
cv2.destroyAllWindows()
