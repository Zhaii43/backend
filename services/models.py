from django.db import models
from django.conf import settings

class WorkSpecification(models.Model):
    service = models.ForeignKey('Service', related_name='work_specifications', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Philippine Peso (PHP)")

    def __str__(self):
        return f"{self.name} (for {self.service.title if self.service else 'No Service'}, PHP {self.price})"

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

class Booking(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    work_specifications = models.ManyToManyField(WorkSpecification, related_name='bookings')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total price in Philippine Peso (PHP)")
    booking_date = models.DateField()
    booking_time = models.TimeField()
    address = models.CharField(max_length=255, help_text="User-selected address for the service")
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude of the selected location")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude of the selected location")
    is_editable = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'booking_date', 'booking_time'],
                name='unique_booking_per_service_datetime'
            )
        ]

    def __str__(self):
        specs = ", ".join(spec.name for spec in self.work_specifications.all())
        return f"Booking for {self.service.title} by {self.user.username} on {self.booking_date} at {self.booking_time} ({specs}, PHP {self.price}, Address: {self.address})"

class Review(models.Model):
    RATING_LABEL_CHOICES = [
        ('Poor', 'Poor'),
        ('Needs Improvement', 'Needs Improvement'),
        ('Average', 'Average'),
        ('Good Job', 'Good Job'),
        ('Excellent Job', 'Excellent Job'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="Rating from 1 to 5")
    rating_label = models.CharField(max_length=50, choices=RATING_LABEL_CHOICES, help_text="Descriptive rating label")
    comment = models.TextField(blank=True, help_text="Customer's review comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.service.title} ({self.rating}/5, {self.rating_label})"

class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='replies')
    comment = models.TextField(blank=True, help_text="Reply to the review")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reply by {self.user.username} to Review {self.review.id}"