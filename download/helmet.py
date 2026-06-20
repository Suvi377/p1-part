
from roboflow import Roboflow
rf = Roboflow(api_key="PfDuZtGT8O7gqfx1r2VE")
project = rf.workspace("sumit-panwar-twic5").project("helmet-detection-nhgqy")
version = project.version(1)
dataset = version.download("yolov8")
                