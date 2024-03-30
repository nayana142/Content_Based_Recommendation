from django.db import models

class Course(models.Model):
    course_title = models.CharField(max_length=255)
    url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_subscribers = models.IntegerField()
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.course_title