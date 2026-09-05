import torch
from transformers import CLIPModel, CLIPProcessor

DEFAULT_CATEGORIES = [
    "a t-shirt",
    "a shirt",
    "a pair of jeans",
    "a pair of trousers",
    "a dress",
    "a jacket",
    "a skirt",
    "a hoodie",
    "a sweater",
    "a kurta",
    "a saree"
]

class ClothingDetector:
    def __init__(self, model_name="openai/clip-vit-base-patch32", categories=None):
        self.categories = categories or DEFAULT_CATEGORIES

        print("Loading CLIP clothing-detection model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model.eval()

        print(f"CLIP loaded on: {self.device}")

    def predict(self, image):
        inputs = self.processor(
            text=self.categories,
            images=image,
            return_tensors="pt",
            padding=True
        )

        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = outputs.logits_per_image.softmax(dim=1)[0]

        predicted_index = probabilities.argmax().item()
        prediction = self.categories[predicted_index]
        confidence = probabilities[predicted_index].item() * 100

        scores = {
            category: round(probabilities[i].item() * 100, 2)
            for i, category in enumerate(self.categories)
        }

        return prediction, confidence, scores
