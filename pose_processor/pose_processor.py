import os
import sys
import tslearn.clustering as ts
import pandas as pd
import numpy as np

CLUSTERS = {
  0: ["Scared", "Disgusted"],
  1: ["Shocked/Angry, eyes wide, mouth wide open"],
  2: ["Crying, Facepalm"],
  3: ["Neutral"],
  4: ["Smiling/Laughing, Thumbs Up, Fist Pump, Peace Sign"]
}

class PoseProcessor():
  def __init__(self):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    build_release_path = dir_path + '/../../openpose/build/python/openpose/Release'
    build_x64_release_path = dir_path + '/../../openpose/build/x64/Release'
    build_bin_path = dir_path + '/../../openpose/build/bin'
    sys.path.append(build_release_path)
    os.environ['PATH'] = os.environ['PATH'] + ';' + build_x64_release_path + ';' + build_bin_path + ';'
    
    try:
      if sys.platform == "win32":
        import pyopenpose as op
      else:
        raise Exception("Non-win32 platform")
      
      self.op = op
      params = dict()
      params["model_folder"] = dir_path + "/../../openpose/models/"
      params["net_resolution"] = "-1x80"
      params["number_people_max"] = 1
      params["face"] = True
      params["hand"] = True
      self.opWrapper = self.op.WrapperPython()
      self.opWrapper.configure(params)
      self.opWrapper.start()
      self.datum = self.op.Datum()

      # Load model
      print("Loading model...")
      self.model = ts.TimeSeriesKMeans.from_json('model/model.json')
      print("Loading model completed")

      self.isLogged = False
    except ImportError as e:
      print("Error: Init PoseProcessor")
      raise e
  
  def get_pose(self, frame):
    datum = self.datum
    datum.cvInputData = frame
    self.opWrapper.emplaceAndPop([datum])
    pose_frame = datum.cvOutputData
    pose_keypoints = datum.poseKeypoints
    hand_keypoints = datum.handKeypoints
    left_hand_keypoints = hand_keypoints[1]
    right_hand_keypoints = hand_keypoints[0]
    face_keypoints = datum.faceKeypoints

    frame_keypoints = {
      "pose": pose_keypoints,
      "lhand": left_hand_keypoints,
      "rhand": right_hand_keypoints,
      "face": face_keypoints
    }

    return pose_frame, frame_keypoints

  def predict(self, frames_keypoints):
    # if not self.isLogged:
      pose_df = create_pose_df()
      face_df = create_face_df()
      l_hand_df = create_hand_df()
      r_hand_df = create_hand_df()
      for frame_keypoints in frames_keypoints:
        pose_keypoints = np.array(frame_keypoints["pose"]).flatten()
        if len(pose_keypoints) > 1: # Pose is detected
          pose_df.loc[len(pose_df.index)] = pose_keypoints
        
        face_keypoints = np.array(frame_keypoints["face"]).flatten()
        # face_keypoints = [0] * 210 # TODO: remove
        if len(face_keypoints) > 1:
          face_df.loc[len(face_df.index)] = face_keypoints

        l_hand_keypoints = np.array(frame_keypoints["lhand"]).flatten()
        if len(l_hand_keypoints) > 1:
          l_hand_df.loc[len(l_hand_df.index)] = l_hand_keypoints

        r_hand_keypoints = np.array(frame_keypoints["rhand"]).flatten()
        if len(r_hand_keypoints) > 1:
          r_hand_df.loc[len(r_hand_df.index)] = r_hand_keypoints
      
      merged_df = pd.concat([pose_df, l_hand_df, r_hand_df, face_df], axis=1, join='inner')
      filter_columns = ["c_", "Toe", "Heel", "Hip", "Knee", "Ankle"]
      for column in filter_columns:
        merged_df.drop(list(merged_df.filter(regex=column)), axis=1, inplace=True)
      
      X = merged_df.to_numpy()
      prediction = self.model.predict(X)
      self.isLogged = True
      print(CLUSTERS[np.bincount(prediction).argmax()])
      result = np.bincount(prediction).argmax()
      return result


# TODO: Duplicated code in model/generate.py
def create_pose_df():
  # https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/media/keypoints_pose_25.png
  PARTS = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "MidHip", "RHip", "RKnee", 
  "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe",
  "RHeel"]
  # x_nose, y_nose, confidence_nose, x_neck, y_neck, confidence_neck...
  columns = []
  for i in range(len(PARTS)):
    part_name = PARTS[i]
    columns.append(f'x_{part_name}')
    columns.append(f'y_{part_name}')
    columns.append(f'c_{part_name}')
  df = pd.DataFrame(columns=columns)
  return df

def create_face_df():
  # https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/media/keypoints_face.png
  columns = []
  for i in range(70):
    columns.append(f'x_{i}')
    columns.append(f'y_{i}')
    columns.append(f'c_{i}')
  df = pd.DataFrame(columns=columns)
  return df

def create_hand_df():
  # https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/media/keypoints_hand.png
  columns = []
  for i in range(21):
    columns.append(f'x_{i}')
    columns.append(f'y_{i}')
    columns.append(f'c_{i}')
  df = pd.DataFrame(columns=columns)
  return df