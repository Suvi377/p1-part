from ultralytics import YOLO

def main():
    print("🚀 Initiating Weapon Detection Training...")
    print("⚠️ IMPORTANT: Plug in your laptop, set power mode to 'Best Performance', and ensure good ventilation!")

    # 1. Load the base YOLOv8 Nano model (Best choice for speed + decent accuracy)
    model = YOLO("yolov8n.pt")

    # 2. Start the Optimized Training
    model.train(
        data="weapon_data.yaml", 
        epochs=50,            # 50 epochs balances solid feature convergence with training time
        imgsz=416,            # The sweet spot: Faster than 640, significantly more accurate than 320
        batch=4,              # Bumping to 8 stabilizes gradients; safe for i5 RAM at 416px
        device="cpu",         # If OpenVINO isn't set up, default to CPU (see acceleration tip below)
        workers=2,            # Matches your i5's performance cores to load data efficiently
        mosaic=1.0,           # Keeps data augmentation active for complex scenes
        augment=True,         # Enables random scaling and translations
        cache=False,          # Avoids RAM throttling on standard laptops
        name="weapon_model_optimized"
    )

if __name__ == "__main__":
    main()
    