import os
import shutil
from ultralytics import YOLO

def train_model(yaml_path, output_name, epochs=50):
    """
    Trains a YOLO model and saves the best weights to your models folder.
    """
    print(f"\n🚀 STARTING TRAINING FOR: {output_name.upper()}...")
    
    # 1. Start with the pre-trained nano model (it learns faster this way)
    model = YOLO('yolov8n.pt')
    
    # 2. Begin the training loop
    # epochs=50 means the AI will look through your entire dataset 50 times to learn
    results = model.train(
        data=yaml_path,
        epochs=epochs,
        imgsz=640,
        batch=16,
        workers=2, # Number of CPU threads to use
        device='cpu', # Change this to '0' if you have an Nvidia GPU
        project='runs/train',
        name=output_name
    )
    
    # 3. Move the finished .pt file to your master models/ folder
    # YOLO saves the best iteration automatically as 'best.pt'
    best_weight_path = f"runs/train/{output_name}/weights/best.pt"
    final_destination = f"models/{output_name}.pt"
    
    if os.path.exists(best_weight_path):
        os.makedirs("models", exist_ok=True)
        shutil.copy(best_weight_path, final_destination)
        print(f"✅ SUCCESSFULLY COMPILED: {final_destination}")
    else:
        print(f"❌ ERROR: Training failed to produce {best_weight_path}")

if __name__ == "__main__":
    # --- IMPORTANT HARDWARE WARNING ---
    # Training all three at once on a laptop will take a VERY long time.
    # Comment out the ones you aren't currently training using the # symbol.
    
    # Train Driver Safety (Helmets / Seatbelts)
    # train_model('training_configs/driver_data.yaml', 'driver_safety', epochs=50)
    
    # Train Public Safety (Weapons / SOS)
    # train_model('training_configs/safety_data.yaml', 'public_safety', epochs=50)
    
    # Train ANPR (License Plates)
    train_model('training_configs/anpr_data.yaml', 'anpr', epochs=50)


    