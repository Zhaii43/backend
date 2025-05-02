from django.db import models

# Popular Business Manager
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category_name}"

# Popular Business Model
class PopularBusiness(models.Model):
    service_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    location = models.TextField()
    image = models.ImageField(upload_to='business_images/', blank=True, null=True)  # Optional image upload


    def __str__(self):
        return f"{self.service_name} ({self.service_category})"
