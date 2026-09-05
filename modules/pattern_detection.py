import torch
from transformers import CLIPModel, CLIPProcessor


PATTERN_CATEGORIES = [
    "plain solid color clothing",
    "striped clothing",
    "checked plaid clothing",
    "floral patterned clothing",
    "polka dot clothing",
    "printed graphic clothing",
    "animal print clothing",
    "abstract patterned clothing"
]


class PatternDetector:

    def __init__(
        self,
        model_name="openai/clip-vit-base-patch32"
    ):

        print("Loading pattern detection model...")

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model = CLIPModel.from_pretrained(
            model_name
        ).to(self.device)

        self.processor = CLIPProcessor.from_pretrained(
            model_name
        )

        self.model.eval()

        print(
            f"Pattern detector loaded on: "
            f"{self.device}"
        )


    def predict(self, image):

        inputs = self.processor(
            text=PATTERN_CATEGORIES,
            images=image,
            return_tensors="pt",
            padding=True
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():

            outputs = self.model(**inputs)

            probabilities = (
                outputs.logits_per_image
                .softmax(dim=1)[0]
            )

        predicted_index = (
            probabilities.argmax().item()
        )

        predicted_pattern = (
            PATTERN_CATEGORIES[
                predicted_index
            ]
        )

        confidence = (
            probabilities[
                predicted_index
            ].item()
            * 100
        )

        scores = {

            pattern: round(
                probabilities[i].item() * 100,
                2
            )

            for i, pattern
            in enumerate(PATTERN_CATEGORIES)

        }

        return (
            predicted_pattern,
            confidence,
            scores
        )