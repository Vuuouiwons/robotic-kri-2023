import cv2 as cv

# Open the default camera
cap = [cv.VideoCapture(0), cv.VideoCapture(2)]

# set resolution
cap[0].set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap[0].set(cv.CAP_PROP_FRAME_HEIGHT, 720)
cap[1].set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap[1].set(cv.CAP_PROP_FRAME_HEIGHT, 720)

# Set the frame rate to 30 fps
cap[0].set(cv.CAP_PROP_FPS, 30)
cap[1].set(cv.CAP_PROP_FPS, 30)

# Define the compression quality
quality = 50

while True:
  # Capture a frame from the camera
  ret2, frame2 = cap[0].read()
  ret1, frame1 = cap[1].read()

  # Check if the frame was captured successfully
  if not ret1 and not ret2:
      break

  # Encode the frame with JPEG compression
  encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]

  result1, encimg1 = cv.imencode('.jpg', frame1, encode_param)
  result2, encimg2 = cv.imencode('.jpg', frame2, encode_param)
  
  # Decode the compressed frame
  decimg1 = cv.imdecode(encimg1, 1)
  decimg2 = cv.imdecode(encimg2, 1)

  # Display the compressed frame
  cv.imshow('Compressed Frame1', decimg1)
  cv.imshow('Compressed Frame2', decimg2)

  # Wait for a key press to exit
  if cv.waitKey(1) & 0xFF == ord('q'):
    break

# Release the camera and close the window
cap[0].release()
cap[1].release()
cv.destroyAllWindows()
