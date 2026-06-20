import cv2

print("🔍 Searching for your webcam...")

# Try indexes 0, 1, 2, and 3
for i in range(4):
    print(f"Testing slot {i}...")
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✅ SUCCESS! Your camera is at index: {i}")
            cv2.imshow("Camera Test - Press ANY KEY to close", frame)
            cv2.waitKey(0)
            cap.release()
            cv2.destroyAllWindows()
            exit()
    cap.release()

print("❌ No cameras found at all. Check your Windows Privacy Settings or physical camera switch!")