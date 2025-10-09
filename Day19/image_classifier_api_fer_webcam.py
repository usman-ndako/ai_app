import cv2
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from PIL import Image

# ------------------------------
# Load Model (directly using resnet18)
# ------------------------------
MODEL_PATH = "resnet_fer_images.pth"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load ResNet18 and adjust final layer for 7 classes
from torchvision.models import resnet18

model = resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 7)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.to(DEVICE)
model.eval()

# ------------------------------
# Image Transform
# ------------------------------
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),  # convert to 3 channels
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# ------------------------------
# FastAPI App
# ------------------------------
app = FastAPI()
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# ------------------------------
# Video Capture
# ------------------------------
cap = cv2.VideoCapture(0)  # 0 = default webcam

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Convert to PIL Image for processing
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        input_tensor = transform(img).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            outputs = model(input_tensor)
            _, pred = torch.max(outputs, 1)
            label = EMOTIONS[pred.item()]

        # Overlay emotion label
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2, cv2.LINE_AA)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(),
                             media_type='multipart/x-mixed-replace; boundary=frame')
