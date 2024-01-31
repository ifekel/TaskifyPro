from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid
from django.utils.text import slugify

now = timezone.now()
naive_datetime = datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
aware_datetime = timezone.make_aware(naive_datetime, timezone=timezone.get_current_timezone())


class Task(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    assigned_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=aware_datetime)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title[:50]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:50])
        super().save(*args, **kwargs)