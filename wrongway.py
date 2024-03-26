from collections import defaultdict
#import supervision as sv

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from numpy import asarray
import cv2
import numpy as np

from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('./best1.pt')

# Open the video file
video_path = "./temp1.mp4"
cap = cv2.VideoCapture(video_path)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width,frame_height)
fps = cap.get(cv2.CAP_PROP_FPS)


output = cv2.VideoWriter("output1.avi", cv2.VideoWriter_fourcc('M','J','P','G'), fps, frame_size)
# Store the track history
track_history = {}
track_history1 = {}
count = {}
last_x = {}
last_y = {}
violation = set()
get_box = {}
#bounding_box_annotator = sv.BoundingBoxAnnotator()

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)
        # Get the boxes and track IDs

        boxes = results[0].boxes.xywh.cpu()
        boxes1 = results[0].boxes.xyxy.cpu()
        if results[0].boxes.id is None:
            continue

        track_ids = results[0].boxes.id.int().cpu().tolist()

        # Visualize the results on the frame

        annotated_frame = results[0].plot()
        # Plot the tracks
        found = {}
        for box, track_id, box1 in zip(boxes, track_ids, boxes1):
            x, y, w, h = box
            x1, y1, x2, y2 = box1
            if count.get(track_id) is None:
                count[track_id] = 0
            if found.get(track_id) is None:
                found[track_id] = 1
            found[track_id] = 1
            if get_box.get(track_id) is None:
                get_box[track_id] = box1
            get_box[track_id] = box1
            count[track_id] += 1
            if track_history.get(track_id) is None:
                track_history[track_id] = x.item()
                last_x[track_id] = x.item()

            if track_history1.get(track_id) is None:
                track_history1[track_id] = y.item()
                last_y[track_id] = y.item()

            last_x[track_id] = max(x.item(), last_x[track_id])
            last_y[track_id] = min(y.item(), last_y[track_id])
        for key, value in track_history.items():
            print(key, value)
        print("\n")
        for key, value in track_history1.items():
            print(key, value)
        print("\n")
        for key, value in last_x.items():
            print(key, value)
        print("\n")
        for key, value in last_y.items():
            print(key, value)
        # Display the annotated frame
        for key, value in track_history.items():
            lst_x = last_x[key]
            lst_y = last_y[key]
            first_x = track_history[key]
            first_y = track_history1[key]
            if count[key] >= 60 and lst_x > first_x and lst_y < first_y and found.get(key) is not None:
                violation.add(key)
                x1, y1, x2, y2 = get_box[key]
                start_point = (int(x1.item()), int(y1.item()))
                end_point = (int(x2.item()), int(y2.item()))
                color = (0, 0, 255)
                thickness = 6
                annotated_frame = cv2.rectangle(annotated_frame, start_point, end_point, color, thickness)
        img = Image.fromarray(annotated_frame)
        print(len(violation))
        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(img)

        # Custom font style and font size
        myFont = ImageFont.truetype("FreeMonoBold.ttf", size=35)
        #myFont = ImageFont.truetype(size=30)
        # Add Text to an image
        s = "Wrong Way Violation Count"
        I1.text((10, 10),s, font=myFont, fill=(0, 0, 255))
        bbox = I1.textbbox((10, 60), str(len(violation)), font=myFont)
        I1.rectangle(bbox, fill="white")
        I1.text((10, 60), str(len(violation)), font=myFont, fill=(0, 0, 255))
        annotated_frame = asarray(img)
        #cv2.imshow("YOLOv8 Tracking", annotated_frame)
        output.write(annotated_frame)
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
output.release()
cv2.destroyAllWindows()