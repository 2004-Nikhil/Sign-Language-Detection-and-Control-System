# Sign Language Detection and Control System

This project aims to create a real-time sign language detection and control system using a Convolutional Neural Network (CNN) model. The system can detect specific hand gestures and perform corresponding actions such as moving the mouse or adjusting the system volume.

## Table of Contents
- [Installation](#installation)
- [Data Collection](#data-collection)
- [Data Splitting](#data-splitting)
- [Model Training](#model-training)
- [Real-Time Detection and Control](#real-time-detection-and-control)
- [Requirements](#requirements)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Sign-Language-Detection-and-Control-System.git
    cd Sign-Language-Detection-and-Control-System
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Data Collection

To collect data for training the model, run the `collectdata.py` script. This script captures images from the webcam and saves them in the specified directories.

```sh
python collectdata.py
```

- Press 'a' to save an image for the 'A' gesture.
- Press 'b' to save an image for the 'B' gesture.
- Press 'c' to save an image for the 'C' gesture.
- Press 'd' to save an image for the 'D' gesture.
- Press 'e' to save an image for the 'E' gesture.
- Press 'f' to save an image for the 'F' gesture.
- Press '.' to save an image for the 'blank' gesture.
- Press 'q' to quit the data collection.

## Data Splitting

To split the collected data into training and validation sets, run the `split.py` script.

```sh
python split.py
```

## Model Training

To train the model, open and run the `trainingModel.ipynb` Jupyter notebook. This notebook includes the following steps:
1. Importing necessary libraries.
2. Loading and preprocessing the data.
3. Defining the CNN model architecture.
4. Training the model.
5. Saving the trained model.

## Real-Time Detection and Control

To run the real-time sign language detection and control system, execute the `realtimedetectioncontrol.py` script.

```sh
python realtimedetectioncontrol.py
```

This script captures video from the webcam, detects hand gestures, and performs corresponding actions such as moving the mouse or adjusting the system volume.

## Requirements

The project requires the following Python packages:

- tensorflow
- opencv-python
- split-folders
- pyautogui
- pycaw
- comtypes

These packages can be installed using the `requirements.txt` file provided in the repository.

```sh
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.