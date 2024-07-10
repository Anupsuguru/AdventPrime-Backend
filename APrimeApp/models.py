import datetime
import uuid
import json
from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Department(BaseModel):
    department_name = models.CharField(max_length=255)
    total_no_of_workshop_conducted = models.IntegerField(default=0)

    def __str__(self):
        return self.department_name


class Category(BaseModel):
    category_name = models.CharField(max_length=255)
    total_no_of_workshop_conducted = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name


class Workshop(BaseModel):
    workshop_name = models.CharField(max_length=255)
    conducted_by = models.CharField(max_length=255)
    conducted_by_department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    workshop_date = models.DateField()
    workshop_start_time = models.TimeField(default=datetime.time(hour=11, minute=0, second=0))
    workshop_end_time = models.TimeField(default=datetime.time(hour=12, minute=0, second=0))
    workshop_location = models.CharField(max_length=255)
    resource = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def clean(self):
        # Ensure that workshop_end_time is greater than workshop_start_time
        if self.workshop_end_time <= self.workshop_start_time:
            raise ValidationError('End time must be after start time.')

    def save(self, *args, **kwargs):
        # Call the clean method to enforce validation rules
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.workshop_name


class Student(BaseModel):
    preferences = models.TextField()
    student_name = models.CharField(max_length=255)
    term = models.CharField(max_length=255)
    course_registered = models.CharField(max_length=255)
    last_login = models.DateTimeField()
    no_of_workshop_attended = models.IntegerField()

    def get_preferences(self):
        return json.loads(self.preferences)

    def set_data(self, value):
        self.preferences = json.dumps(value)

    def __str__(self):
        return self.student_name


class Registration(BaseModel):
    waitlist = models.TextField()
    confirmed_registration = models.TextField()
    total_seats = models.IntegerField()
    seats_filled = models.IntegerField()
    seats_available = models.IntegerField()
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)


    def get_waitlist(self):
        return json.loads(self.waitlist)

    def set_waitlist(self, value):
        self.waitlist = json.dumps(value)

    def get_confirmed_registration(self):
        return json.loads(self.confirmed_registration)

    def set_confirmed_registration(self, value):
        self.confirmed_registration = json.dumps(value)

    def __str__(self):
        return self.id
