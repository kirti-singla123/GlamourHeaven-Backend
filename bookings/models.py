from django.db import models

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
        # Automatically prepend +91 if missing (for India)
        if not self.phone.startswith('+'):
            digits_only = ''.join(filter(str.isdigit, self.phone))
            self.phone = f'+91{digits_only}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} – {self.service} on {self.date} {self.time}"
