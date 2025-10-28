from django.db import models

class BillImage(models.Model):
    image_path = models.CharField(max_length=255, unique=True)
    ocr_text = models.TextField(blank=True, null=True)
    embedding = models.JSONField(blank=True, null=True)  # store list of floats
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_path
