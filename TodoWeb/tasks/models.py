from django.conf import settings
import mongoengine
from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime

# Custom User model using mongoengine
class User(Document):
    username = StringField(required=True, unique=True, max_length=150)
    password = StringField(required=True)
    email = StringField(required=False)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    date_joined = DateTimeField(default=datetime.utcnow)
    
    meta = {'collection': 'users'}
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_username(self):
        return self.username
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username

# Task model using mongoengine
class Task(Document):
    title = StringField(required=True, max_length=200)
    description = StringField()
    due_date = DateTimeField()
    completed = BooleanField(default=False)
    user = ReferenceField(User, required=True)

    meta = {'collection': 'tasks'}
