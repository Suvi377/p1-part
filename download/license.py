
from roboflow import Roboflow
rf = Roboflow(api_key="PfDuZtGT8O7gqfx1r2VE")
project = rf.workspace("seydoudansogo").project("lisence-agzmg")
version = project.version(1)
dataset = version.download("yolov8")
                