from ultralytics import YOLO

def main():
    print("🛵 Initiating Fast & Balanced CPU Training for Helmet Detection...")
    print("⚠️  IMPORTANT: Plug in your laptop and keep it cool!")

    # 1. Load the lightweight YOLOv8 Nano base model
    model = YOLO("yolov8n.pt")

    # 2. Start the optimized training process
    model.train(
        data=r"C:\Users\Suvidhi\Desktop\p1 part\Helmet-Detection-1\helmet.yaml", # Your map file
        epochs=50,                  # 50 epochs balances solid accuracy with reasonable CPU time
        imgsz=416,                  # 🧠 SWEET SPOT: Twice as fast as 640, significantly sharper than 320 for small helmets
        batch=8,                    # Stable batch size for system RAM at 416px
        workers=2,                  # Utilizes your i5's performance cores cleanly
        device="cpu",               # Standard CPU execution
        patience=10,                # Early stopping if the model plateaus for 10 epochs
        mosaic=1.0,                 # Keeps data augmentation active to mix classes into complex scenes
        augment=True,               # Forces random scaling, translations, and color shifts
        cache=False,                # Keeps your laptop's system RAM from throttling
        name="helmet_model_fast",   # Optimized folder name in runs/detect/
        verbose=True
    )

if __name__ == "__main__":
    main()