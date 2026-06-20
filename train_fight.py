import os
from ultralytics import YOLO

def main():
    # Points to your existing fight dataset using the absolute path
    yaml_path = r"C:\Users\Suvidhi\Desktop\p1 part\fight-detection-1\data.yaml" 
    
    # Start fresh with the base nano model
    base_model = YOLO("yolov8n.pt")
    
    print("🚀 Initiating Fast & Balanced CPU Training for Fight Detection...")
    print("⚠️  IMPORTANT: Plug in your laptop and elevate it for maximum cooling!")
    
    base_model.train(
        data=yaml_path,
        epochs=50,          # 50 loops is great for multi-class/action variance
        imgsz=416,          # 🧠 SWEET SPOT: Much faster than 640, significantly sharper than 320
        batch=8,            # Bumping to 8 stabilizes gradient descent and works great with 416px
        workers=2,          # Uses 4 data loader threads to match your i5's performance cores
        device="cpu",       # Standard CPU fallback execution
        patience=10,        # Early stopping if the model stops improving for 10 epochs
        mosaic=1.0,         # Keeps data augmentation active (crucial for overlapping bodies in fights)
        augment=True,       # Randomly transforms images to prevent overfitting
        cache=False,        # Keeps your laptop system RAM from choking
        name="fight_model_fast"
    )
    
    print("\n🎉 Fast Training Complete! Your fight detection model is fully baked.")

if __name__ == "__main__":
    main()