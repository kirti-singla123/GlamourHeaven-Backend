from django.db import models


def format_phone_number(phone):
    # Normalize to E.164 for Canada/US (+1)
    cleaned = phone.replace(' ', '').replace('-', '')

    if cleaned.startswith('+'):
        return cleaned
    if cleaned.startswith('1'):
        return f'+{cleaned}'
    if len(cleaned) == 10 and cleaned.isdigit():
        return f'+1{cleaned}'
    return cleaned


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=120)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.phone = format_phone_number(self.phone)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} – {self.service} on {self.date} {self.time}"
