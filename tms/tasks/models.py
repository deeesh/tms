from django.db import models
from django.contrib.auth.models import User, Permission


TASK_STATUS = (
    ("New", "New"),
    ("Started", "Started"),
    ("Progress", "Progress"),
    ("Review", "Review"),
    ("Completed", "Completed"),
)

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length= 50, choices= TASK_STATUS, default= "New")
    
    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ("can_mark_complete", "Can mark task as complete"),
            ("can_update_task", "Can update task details"),
            ("can_view_task_description", "Can view Task Description" ),
            ("can_create_task", "Can Create Task")
        ]
