import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn

# =========================
# Config
# =========================
DEVICE = "cpu"  # or "cuda" if GPU available
MODEL_PATH = "resnet_fer_images.pth"  # your saved model
NUM_CLASSES = 7  # FER dataset classes: ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# =========================
# Initialize model
# =========================
model = models.resnet18(weights=None)  # no pretrained weights
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval()
model.to(DEVICE)

# Emotion labels
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# =========================
# Image transforms
# =========================
transform = transforms.Compose([
    transforms.Resize((48, 48)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],  # standard for resnet
                         std=[0.229, 0.224, 0.225])
])

# =========================
# FastAPI app
# =========================
app = FastAPI(title="Facial Emotion Recognition API")

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Read image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Transform
        img_tensor = transform(image).unsqueeze(0).to(DEVICE)

        # Predict
        with torch.no_grad():
            outputs = model(img_tensor)
            _, predicted = torch.max(outputs, 1)
            emotion = EMOTIONS[predicted.item()]

        return JSONResponse({"emotion": emotion})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# =========================
# Root endpoint
# =========================
@app.get("/")
def read_root():
    return {"message": "Facial Emotion Recognition API is running. Use /predict/ endpoint."}

# =========================
# To run:
# uvicorn image_classifier_api_fer:app --reload
# =========================
