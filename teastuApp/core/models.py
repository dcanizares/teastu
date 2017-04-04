from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.student.save()


class Interview(BaseModel):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    contents = models.CharField(max_length=1000)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Work(models.Model):
    title = models.CharField(max_length=30)
    settlement = models.CharField(max_length=100)
    deadline = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


# class WorkTeam(models.Model):
#     publications = models.ManyToManyField(Publication)

#     def __str__(self):
#         return self.headline

#     class Meta:
#         ordering = ('headline',)
