
from roboflow import Roboflow
rf = Roboflow(api_key="PfDuZtGT8O7gqfx1r2VE")
project = rf.workspace("swifeye").project("weapon-c6q7e")
version = project.version(9)
dataset = version.download("yolov8")
                