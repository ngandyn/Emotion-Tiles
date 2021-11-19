import cv2
import time
from pose_processor.pose_processor import PoseProcessor

MAX_FRAMES = 10
FEED_HEIGHT = 200
FEED_WINDOW_SIZE = (200, 200)
FRAME_RATE = 5 #frames per second

class Camera():
  def __init__(self, webcam_ip=None):
    if webcam_ip:
      # Third party web cam
      self.cam = cv2.VideoCapture(f'http://{webcam_ip}/video')
    else:
      # Built in camera
      self.cam = cv2.VideoCapture(0)
    self.camera_ratio = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH) / self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    self.lastUpdate = time.time()

    # Pose processor
    self.pose_processor = PoseProcessor()
    self.frames_keypoints = [] # List of frames keypoints {pose, lhand, rhand, face}


  def update(self):
    currentTime = time.time()
    ret, frame = self.cam.read()
    if currentTime > self.lastUpdate + 1/FRAME_RATE:
      frame = cv2.flip(frame, 1) # Let's only store the smaller frame
      frame_small = cv2.resize(frame, (int(FEED_HEIGHT*self.camera_ratio), FEED_HEIGHT))
      pose_frame, frame_keypoints = self.pose_processor.get_pose(frame_small)
      cv2.imshow('frame', pose_frame)
      self.store_frame_keypoints(frame_keypoints)
      self.lastUpdate = time.time()
      if len(self.frames_keypoints) >= MAX_FRAMES:
        prediction = self.pose_processor.predict(self.frames_keypoints)
        return prediction


  def store_frame_keypoints(self, pose):
    if len(self.frames_keypoints) >= MAX_FRAMES:
      self.frames_keypoints.pop(0)
    self.frames_keypoints.append(pose)

  def destroy(self):
    self.cam.release()
    cv2.destroyAllWindows()