from subprocess import call
import os
import zipfile
import json
import pandas as pd

def gif_to_json_pose():
  emotion_type = 'fear' # Change this to "fear" "sadness" "surprise" later
  input_path = f'../dataset/{emotion_type}'
  openpose_portable_path = '../../Portable-Demo/openpose/'
  output_path = '../dataset/pose_outputs'

  if not os.path.exists(output_path):
    os.makedirs(output_path)

  if not os.path.exists(f'{output_path}/{emotion_type}'):
    os.makedirs(f'{output_path}/{emotion_type}')

  for filename in os.listdir(input_path):
    if filename.endswith(".gif"):
      name = os.path.splitext(filename)[0] # no extension
      bash_command = f'"{openpose_portable_path}/bin/OpenPoseDemo.exe" ' + \
        f'--video {input_path}/{filename} ' + \
        f'--net_resolution "320x320" ' + \
        f'--write_json {output_path}/{emotion_type}/{name} ' + \
        f'--display 0 ' + \
        f'--render_pose 0 ' + \
        f'--number_people_max 1 ' + \
        f'--face ' + \
        f'--hand ' + \
        f'--model_folder {openpose_portable_path}/models '
      print("Running: ", bash_command)
      call(bash_command, shell=True)

def json_pose_to_csv():
  # Extract the pose_outputs.zip
  pose_outputs_path = "./pose_outputs"
  if not os.path.exists(pose_outputs_path):
    with zipfile.ZipFile("./pose_outputs.zip", 'r') as zip_ref:
      zip_ref.extractall()
  
  pose_csv_outputs_path = "./pose_csv_outputs"
  if not os.path.exists(pose_csv_outputs_path):
    os.makedirs(pose_csv_outputs_path)

  emotion_types = ["fear", "happiness", "sadness", "surprise"]
  for emotion_type in emotion_types:
    for folder_name in os.listdir(f'{pose_outputs_path}/{emotion_type}'):
      if not os.path.exists(f'{pose_csv_outputs_path}/{emotion_type}/{folder_name}'):
        os.makedirs(f'{pose_csv_outputs_path}/{emotion_type}/{folder_name}')
      
      # Create empty data frames
      gif_pose_df = create_pose_df()
      gif_face_df = create_face_df()
      gif_hand_left_df = create_hand_df()
      gif_hand_right_df = create_hand_df()

      # Go through the json files and store the data into the data frames
      for file_name in os.listdir(f'{pose_outputs_path}/{emotion_type}/{folder_name}'):
        with open(f'{pose_outputs_path}/{emotion_type}/{folder_name}/{file_name}') as json_file:
          data = json.load(json_file)
          if len(data['people']) > 0:
            person = data['people'][0]
            pose_keypoints = person['pose_keypoints_2d']
            face_keypoints = person['face_keypoints_2d']
            hand_left_keypoints = person['hand_left_keypoints_2d']
            hand_right_keypoints = person['hand_right_keypoints_2d']
            gif_pose_df.loc[len(gif_pose_df.index)] = pose_keypoints
            gif_face_df.loc[len(gif_face_df.index)] = face_keypoints
            gif_hand_left_df.loc[len(gif_hand_left_df.index)] = hand_left_keypoints
            gif_hand_right_df.loc[len(gif_hand_right_df.index)] = hand_right_keypoints
      
      # Export the data frames to csv
      gif_pose_df.to_csv(f'{pose_csv_outputs_path}/{emotion_type}/{folder_name}/pose.csv')
      gif_face_df.to_csv(f'{pose_csv_outputs_path}/{emotion_type}/{folder_name}/face.csv')
      gif_hand_left_df.to_csv(f'{pose_csv_outputs_path}/{emotion_type}/{folder_name}/hand_left.csv')
      gif_hand_right_df.to_csv(f'{pose_csv_outputs_path}/{emotion_type}/{folder_name}/hand_right.csv')

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



#gif_to_json_pose()
json_pose_to_csv()