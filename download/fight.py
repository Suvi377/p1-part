#!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="PfDuZtGT8O7gqfx1r2VE")
project = rf.workspace("mouse-dataset").project("fight-detection-29tz7")
version = project.version(1)
dataset = version.download("yolov8")
                