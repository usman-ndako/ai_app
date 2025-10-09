README.md
# Day 19: Facial Emotion Recognition (FER) with ResNet18

## Project Overview
This project implements a **Facial Emotion Recognition** model using **PyTorch ResNet18**. The trained model is served via **FastAPI** for local image predictions.

---

## Folder Structure



day19/
│
├── train/ # Training images, organized by emotion folders
├── test/ # Test images, organized by emotion folders
├── resnet_fer_images.pth # Trained model weights
├── image_classifier_api_fer.py # FastAPI server script
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## Setup Instructions

1. **Clone or copy the Day 19 folder** locally.
2. **Install dependencies**:

```bash
pip install -r requirements.txt


Run the FastAPI server:

python image_classifier_api_fer.py


Test the API:

Open Swagger UI: http://127.0.0.1:8000/docs

Use the /predict/ endpoint to send images and get emotion predictions.

Model Info

Architecture: ResNet18 (modified for 7 emotion classes)

Dataset: FER dataset from Kaggle

Transforms: Resize to 48x48, normalization, convert to tensor

Checkpoint: resnet_fer_images.pth

Notes

Partial training is allowed if full epochs are not completed; the saved .pth file can be used to continue training or inference.

For reproducibility, ensure your input images undergo the same transformations as used during training.

FastAPI requires Python >=3.10 and PyTorch 2.x.