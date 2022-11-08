'''
Crosswalk detected model main file

You must download Yolov5
--------------How to download YOLOv5----------------
git clone https://github.com/ultralytics/yolov5.git
----------------------------------------------------

After downloading, you need to move this file into the YOLOv5 folder.

Edited by Heerae Lee
9th Nov 2022
'''

import os
import sys
import cv2
from pathlib import Path
import time
from threading import Thread
import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import LoadImages
from utils.general import (LOGGER, Profile, check_img_size, colorstr, cv2,
                           non_max_suppression, scale_boxes)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device

class VideoStream:
    """Camera object that controls video streaming from the WebCamera"""

    def __init__(self, resolution=(640, 480), framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])

        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

        # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
        # Start the thread that reads frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Return the most recent frame
        return self.frame

    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True

source = "/home/pi/Ada/crosswalk_model/stream/img.jpg"     # image path to detect -> image saved from stream
weights = "/home/pi/Ada/crosswalk_model/best-int8-64.tflite"    # model weight path
project = "/home/pi/Ada/crosswalk_model/result/"    # folder path where detection images are saved
txt_filename = "/home/pi/Ada/crosswalk_model/crosswalk_result.txt"      # txt file path where the detection result is saved
imgsz = (64, 64)  # inference size (height, width)
max_det = 10  # maximum detections per image
device = ''  # cuda device, i.e. 0 or 0,1,2,3 or cpu
img_name = 'detect.jpg'  # save results to project/name
line_thickness = 3  # bounding box thickness (pixels)
hide_labels = False  # hide labels
hide_conf = True  # hide confidences

# start video stream
videostream = VideoStream(resolution=imgsz,framerate=30).start()
time.sleep(1)

# Load model
device = select_device(device)
model = DetectMultiBackend(weights, device=device)
stride, detect_name, pt = model.stride, 'crosswalk', model.pt
imgsz = check_img_size(imgsz, s=stride)  # check image size
model.warmup(imgsz=(1 if pt or model.triton else 1, 3, *imgsz))  # warmup

# After loading the model, save 'start' to a text file
file = open(txt_filename, 'w')
file.write(' start\n')
file.close()

cnt=0

while True:
    file = open(txt_filename, 'a')
    frame1 = videostream.read()
    frame = frame1.copy()
    cv2.imwrite(source, frame)

    save_img = not source.endswith('.txt')  # save inference images

    # Directories
    save_dir = project

    # Dataloader
    bs = 1  # batch_size
    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    #model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            pred = model(im, augment=False, visualize=False)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, max_det=max_det)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = save_dir + img_name  # im.jpg
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            annotator = Annotator(im0, line_width=line_thickness, example=str(detect_name))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {img_name}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (detect_name if hide_conf else f'{detect_name} {conf:.2f}')
                        annotator.box_label(xyxy, label, color=colors(c, True))

            # img results
            im0 = annotator.result()

            # Save results (image with detections)
            if save_img:
                cv2.imwrite(save_path, im0)

        # Print time (inference-only)
        LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

        # Add result to txt file
        if len(det):
            file.write(f'True {cnt}\n')
        else:
            file.write(f'False {cnt}\n')
        
        file.close()

    cnt += 1
    img = cv2.imread(project + img_name)
    cv2.imshow('frame', img)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        videostream.stop()
        break

# Print results
t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
if save_img:
    LOGGER.info(f"Results saved to {colorstr('bold', save_dir)} ")