import torch
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
from torchvision import transforms, models
from sklearn.metrics.pairwise import cosine_similarity
ocr = PaddleOCR(lang='en')

# Pretrained model for embeddings (ResNet50)
resnet = models.resnet50(pretrained=True)
resnet.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# def extract_ocr_text(image_path):
#     result = ocr.predict(image_path)
#     text = "".join([line[1][0] for line in result[0]])
#     return text
# def extract_ocr_text(image_path):
#     from paddleocr import PaddleOCR

#     ocr = PaddleOCR(use_angle_cls=True, lang='en')  # initialize only once ideally
#     result = ocr.ocr(image_path, cls=True)

#     text_lines = []
#     for line in result:
#         for part in line:
#             text_lines.append(part[1][0])  # part[1][0] = text string

#     text = " ".join(text_lines)
#     return text

def extract_ocr_text(image_path):
    from easyocr import Reader
    reader = Reader(['en'])
    result = reader.readtext(image_path)

    text = " ".join([line[1] for line in result])
    return text

def get_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        features = resnet(tensor)
    return features[0].numpy().tolist()

def cosine_sim(vec1, vec2):
    return cosine_similarity([vec1], [vec2])[0][0]

def text_similarity(text1, text2):
    set1, set2 = set(text1.lower().split()), set(text2.lower().split())
    return len(set1 & set2) / max(1, len(set1 | set2))
