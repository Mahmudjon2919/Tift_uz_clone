from django.db import models


class Region(models.Model):
    title=models.CharField(max_length=255)
    order_id=models.IntegerField(unique=True)

    def __str__(self):
        return self.title


    class Meta:
        ordering=("order_id", "id")

class District(models.Model):
    title=models.CharField(max_length=255)
    region=models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts")
    order_id = models.IntegerField(unique=True,)

    def __str__(self):
        return self.title

    class Meta:
        ordering=("order_id", "id")

class Social(models.Model):
    class SocialMediaChoices(models.TextChoices):
       TELEGRAM="telegram", "telegram"
       INSTAGRAM="instagram", "Instagram"
       FACEBOOK="facebook", "Facebook"
       YOUTUBE="youtube", "Youtube"
    title=models.CharField(max_length=255)
    social=models.CharField(choices=SocialMediaChoices.choices, max_length=16)
    link=models.URLField()