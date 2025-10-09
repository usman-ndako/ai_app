# image_classifier_api.py

# --------------------------
# Step 0: Imports
# --------------------------
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import io

# --------------------------
# Step 1: Define CNN Model
# --------------------------
class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.dropout2(x)
        x = self.fc2(x)
        return x

# --------------------------
# Step 2: Load trained model
# --------------------------
model = CNNModel()
model.load_state_dict(torch.load('mnist_cnn.pth', map_location=torch.device('cpu')))
model.eval()  # evaluation mode

# --------------------------
# Step 3: Image Preprocessing
# --------------------------
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28,28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return transform(image).unsqueeze(0)  # add batch dimension

# --------------------------
# Step 4: Create FastAPI App
# --------------------------
app = FastAPI(title="MNIST Image Classifier API")

@app.get("/")
def home():
    return {"message": "MNIST Image Classifier API is running."}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        tensor = preprocess_image(image_bytes)
        outputs = model(tensor)
        _, predicted = torch.max(outputs.data, 1)
        return JSONResponse({"prediction": int(predicted.item())})
    except Exception as e:
        return JSONResponse({"error": str(e)})