import os,time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import BillImage
from .serializers import BillImageSerializer
from .utils import extract_ocr_text, get_image_embedding, cosine_sim, text_similarity
MEDIA_ROOT = os.path.join(settings.BASE_DIR, "media")
class BillCompareView(APIView):
    def post(self, request):
        file = request.FILES.get('image')
        if not file:
            return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        image_path = os.path.join(MEDIA_ROOT, str(time.time())+file.name)
        with open(image_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        embedding = get_image_embedding(image_path)
        sim_text = ""
        for existing in BillImage.objects.all():
            if existing.embedding:
                sim_embed = cosine_sim(embedding, existing.embedding)
            else:
                sim_embed = 0
            if sim_embed > 0.95:
                return Response({
                    "message": "Image already exists",
                    "matched_image": existing.image_path,
                    "ocr_similarity": sim_text,
                    "embedding_similarity": sim_embed
                })
        ocr_text = extract_ocr_text(image_path)
        for existing in BillImage.objects.all():
            if existing.ocr_text:
                sim_text = text_similarity(ocr_text, existing.ocr_text)
            else:
                sim_text = 0
            
            if sim_text > 0.9:
                return Response({
                    "message": "Image already exists",
                    "matched_image": existing.image_path,
                    "ocr_similarity": sim_text,
                    "embedding_similarity": sim_embed
                })
        BillImage.objects.create(
            image_path=str(time.time())+file.name,
            ocr_text=ocr_text,
            embedding=embedding
        )
        return Response({
            "message": "New image stored successfully",
            "ocr_text": ocr_text[:150] + "...",
            "enbeding": str(embedding[:150]) + "...",
        })