from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    category = models.CharField(max_length=100, null=False, blank=False)
    num_of_products = models.IntegerField()

    def __str__(self):
        return f'{self.category} - {self.num_of_products}'


class UserAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10, 
        choices=[('present', 'Present'), ('absent', 'Absent')],
        default='absent'
    )

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['user__username', '-date']  # Order by username, then date descending

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.status}'


    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']  # Optional: Order by date descending

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.status}'
