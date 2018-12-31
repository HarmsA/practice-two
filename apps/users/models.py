from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate(self, form):
        errors = []
        try:
            user = self.get(email=form['email'])
            if not bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                errors.append("Email or password is bad")
        except:
            errors.append('Email or password is bad')
        if len(errors)>0:
            return False
        else:
            return True

    def register_validate(self, form):
        errors = []
        if len(form['f_name'])<2:
            errors.append('First name is to short.')
        if len(form['l_name'])<2:
            errors.append('Last name is to short.')
        if len(form['password'])<2:
            errors.append('Password is to short.')

        if not EMAIL_REGEX.match(form['email']):
            errors.append('Email must be valid')
        email_list = self.filter(email=form['email'])
        if len(email_list) > 0:
            errors.append('Email already in use')

        if form['password'] != form['confirm_password']:
            errors.append('Password must match the Confirm password')
        return errors


    def create_user(self, form):
        pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        user = self.create(
            f_name=form['f_name'],
            l_name=form['l_name'],
            email=form['email'],
            password=pw_hash,
        )
        return user


class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class JobManager(models.Manager):
    def addjob_verify(self, form):
        errors = []
        if len(form['title'])<3:
            errors.append('Must have a title for the Job')
        if len(form['description'])<10:
            errors.append('Must have a description for the Job')
        if len(form['location']) < 1:
            errors.append('Must have a location for the Job')
        return errors

    def create_job(self, form, user_id):
        user = User.objects.get(id=user_id)
        job = self.create(
            location = form['location'],
            description = form['description'],
            title = form['title'],
            creator = user,
        )
        return job


class Job(models.Model):
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='job')
    worker = models.ForeignKey(User, related_name='assigned_job', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
