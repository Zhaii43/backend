from django.db import models

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('cleaning', 'Cleaning'),
        ('repair', 'Repair'),
        ('painting', 'Painting'),
        ('plumbing', 'Plumbing'),
        ('electric', 'Electric'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='cleaning')
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_images/')

    def __str__(self):
        return f"Image for {self.service.title}"
