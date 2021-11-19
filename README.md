# Emotion-Tiles

## File Structure
* main.py: entry point to the game
* download_dataset.py: downloads gif dataset from GIFGIF (http://gifgif.media.mit.edu/)
* /model folder
  * generate.py: converts gif to json files using OpenPose
  * model_generate.ipynb:
  * model.json: the model generated from the jupyter/colab notebook
  * pose_csv_outputs.zip: the pose/face/hands keypoints in csv format
  * pose_outputs.zip: the pose/face/hands keypoints in json format (OpenPose only exports json files)
* /camera folder
  * Camera.py: for handling camera video feed. It takes the frames to the /pose_processor/pose_processor.py for social signal prediction
* /pose_processor folder
  * pose_processor.py: Initializes OpenPose. Extract keypoints from frames. Predict the social signal based on the model in /model/model.json
* /game folder
  * Game logic to update and render the game
  * Game.py: handles the states, inputs, render
  * Colors.py: color constants
  * Scoreboard.py: keeps track of score
  * Tile.py: Manages tile


## Self-evaluation
Overall, we are happy about how the project turned out. We tried to do what was said in the proposal and midterm presentation, which was to create a piano-tile type of game using social signal detection as inputs in real-time. However, there were some limitations that forced us to simplify the program. One of the limitations was the accuracy of the model. We tried different approaches (e.g: cleaning the cartoons in the dataset, removing features, scaling...etc) to train the model, but the prediction did not have the best accuracy. Another limitation was using OpenPose in real-time. OpenPose required a powerful machine to accurately and efficiently detect the poses/face/hands. Initially, we used CPU (because our team members had different GPU: AMD and Nvidia) to run OpenPose, but the performance was terrible (It took ~10 seconds to process 1 frame). Then, we compiled and switched to the OpenPose CUDA version and the performance improved significantly. Unfortunately, detecting all features (pose/face/hands) was very GPU memory intensive. Only one of us had a GPU that was powerful enough to run it (A GTX 1060 3GB did not have enough memory). As a result, it became difficult to develop and test more game features. Lastly, we spent a lot of time installing and compiling OpenPose because it was unexpectedly complicated due to versionings (E.g: Python 3.8 did not work, Python 3.7 worked but required 64 bits depending on compiler... etc).



## Special Dependencies
* OpenPose Python API
  * Used to do real-time pose keypoints extraction
  * Installation (Windows):
    * Requirements:
      * cmake GUI
      * Visual Studio 2019 with Desktop development with C++
      * CUDA (Nvidia)
      * Python 3.7 (64-bits depending on the compiler version)
    * Steps:
      * Clone OpenPose repo (https://github.com/CMU-Perceptual-Computing-Lab/openpose) following the OpenPose relative path requirement below
      * Open cmake GUI
      * Set "Where is the source code" to /openpose path
      * Set "Where to build the binaries" to /openpose/build path
      * Click Configure and select Visual Studio 2019
      * Check BUILD_PYTHON
      * Click generate
      * Open build/OpenPose.sln in Visual Studio 2019
      * Build the project in Release
* OpenPose Executable
  * Used to do pose keypoints extraction on large gif dataset
  * Installation:
    * https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases

&nbsp;   OpenPose relative path requirement:<br />
&nbsp;   &nbsp;  | -- Emotion-Tiles<br />
&nbsp;   &nbsp;  | -- openpose<br />


## How to run
* python main.py
* Alternative camera (IP Webcam)
  * https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_CA
  * For those who want to use phone as camera
  * Option: --webcam IP:PORT
  * E.g: --webcam 192.168.0.12:8080
* We tested it using the command: python main.py  --webcam 192.168.0.13:8080
# Emotion-Tiles
