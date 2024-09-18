from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from apps.common.models import District
from apps.education.models import Direction
from django.urls import reverse



class Gender(models.TextChoices):
    MALE = "male", "Erkak"
    FEMALE = "female", "Ayol"

class ApplicationStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class Application(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    passport=models.CharField(max_length=9)
    pinfl=models.CharField(max_length=14)
    gender=models.CharField(max_length=6, choices=Gender.choices)
    birth_date=models.DateField()
    direction=models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True,blank=True)
    status=models.CharField(max_length=16, choices=ApplicationStatusChoices.choices)
    district=models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    contract_url=models.CharField(max_length=255, null=True, blank=tuple)

    accepted_at=models.DateTimeField(null=True, blank=True)
    created=models.DateTimeField(auto_now=True)

    def __str__(self) ->str:
        return f"(self.first_name) (self.last_name)"

    def save(self, *args, **kwargs) -> None:
        from weasyprint import HTML
        from django.conf import settings
        import os

        if (
                self.status == ApplicationStatusChoices.ACCEPTED or self.status == ApplicationStatusChoices.REJECTED) and not self.accepted_at:
            if self.status == ApplicationStatusChoices.ACCEPTED:
                if not os.path.exists("contracts"):
                    os.makedirs("contracts")


                file_name = f"contracts/{self.first_name}-{self.last_name}.pdf"

                HTML(f"{settings.HOST_NAME}{reverse('application_generator')}?application_id={self.pk}").write_pdf(
                    file_name)

                self.contract_url = file_name

            self.accepted_at = datetime.now()
        return super().save(*args, **kwargs)
