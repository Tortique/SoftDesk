from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=32)

    is_active = models.BooleanField(default=True)


class Contributors(models.Model):
    ROLE = (
        ('AUTEUR', 'auteur'),
        ('MEMBRE', 'membre'),
    )
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.Choices
    role = models.CharField(max_length=15, choices=ROLE, default='MEMBRE')


class Projects(models.Model):
    PROJECT_TYPE = (
        ("BACK_END", "back_end"),
        ("FRONT_END", "front_end"),
        ("IOS", "ios"),
        ("ANDROID", "android")
    )
    title = models.CharField(max_length=164)
    description = models.CharField(max_length=2160)
    type = models.CharField(max_length=15, choices=PROJECT_TYPE)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Issues(models.Model):
    TAG = (
        ("BUG", "bug"),
        ("AMELIORATION", "amélioration"),
        ("TACHE", "tâche")
    )
    PRIORITY = (
        ("FAIBLE", "faible"),
        ("MOYENNE", "moyenne"),
        ("ELEVEE", 'élevée')
    )
    STATUS = (
        ("A FAIRE", "à faire"),
        ("EN COURS", "en cours"),
        ("TERMINE", "terminé")
    )
    title = models.CharField(max_length=15)
    desc = models.CharField(max_length=150)
    tag = models.CharField(max_length=15, choices=TAG, default="TACHE")
    priority = models.CharField(max_length=15, choices=PRIORITY, default="FAIBLE")
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE, related_name='issue_project')
    status = models.CharField(max_length=15, choices=STATUS, default="A FAIRE")
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='issue_author')
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=150)
    author_user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comment_author')
    issue_id = models.ForeignKey('api.Issues', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
