from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField(unique=True)
	roll_number = models.CharField(max_length=20, unique=True)
	enrollment_date = models.DateField(null=True, blank=True)

	class Meta:
		ordering = ['last_name', 'first_name']

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.roll_number})"


class Feedback(models.Model):
    RATING_CHOICES = [(i, f"{i} ★") for i in range(1, 6)]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feedbacks',
    )
    subject = models.CharField(max_length=120)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True,
        help_text="Optional 1–5 star rating",
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"[{self.subject}] by {self.user.username}"
