import os
import shutil
from ultralytics import YOLO

def setup_test_models():
    # 1. Ensure the models directory exists
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)
    
    print("📥 Downloading base YOLOv8 nano model from Ultralytics...")
    # This triggers an automatic download of the official yolov8n.pt file
    base_model = YOLO('yolov8n.pt')
    
    # 2. Define the target files your omniguard_main.py expects
    target_models = ['public_safety.pt', 'driver_safety.pt', 'anpr.pt']
    
    print("\n📦 Duplicating and renaming models for the test environment...")
    for model_name in target_models:
        target_path = os.path.join(models_dir, model_name)
        
        # Copy the downloaded yolov8n.pt to create dummy files
        shutil.copy('yolov8n.pt', target_path)
        print(f"  └── Created: {target_path}")
        
    print("\n✅ Setup Complete! Your models folder is populated.")
    print("🚀 You can now run: python omniguard_main.py")

if __name__ == "__main__":
    setup_test_models()