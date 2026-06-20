from ultralytics import YOLO

def main():
    print("🚗 Initiating Fast & High-Readability CPU Training for License Plates...")
    print("⚠️  IMPORTANT: Plug in your laptop and keep it cool!")

    # 1. Load the lightweight YOLOv8 Nano base model
    model = YOLO("yolov8n.pt")

    # 2. Start the optimized training process
    model.train(
        data=r"C:\Users\Suvidhi\Desktop\p1 part\License-1\license_data.yaml", # Path to your map file
        epochs=50,                  # 50 epochs balances high text recognition with CPU processing time
        imgsz=512,                  # 🔍 TEXT OPTIMIZED: Bigger than 320/416 so characters don't pixelate, but faster than 640
        batch=4,                    # Kept at 4 because 512px images consume slightly more RAM on CPU
        workers=2,                  # Utilizes your i5's performance cores cleanly
        device="cpu",               # Explicitly handles CPU training
        patience=10,                # Stops training early if validation loss plateaus for 10 epochs
        mosaic=1.0,                 # Keeps data augmentation active to mix classes into complex scenes
        augment=True,               # Forces random scaling, translations, and color shifts
        cache=False,                # Keeps your laptop's system RAM from throttling
        name="plate_model_fast",    # Optimized folder name in runs/detect/
        verbose=True
    )

if __name__ == "__main__":
    main()
    