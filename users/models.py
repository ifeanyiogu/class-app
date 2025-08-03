from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    phone = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        help_text="Phone number with country code (e.g., +14155552671)"
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
        
    def clean(self):
        super().clean()

        # Enforce at least one of email or phone
        if not self.email and not self.phone:
            raise ValidationError("Either email or phone must be provided.")

    def save(self, *args, **kwargs):
        self.full_clean()  # ensures `clean()` is called
        super().save(*args, **kwargs)