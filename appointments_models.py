from django.db import models
from django.contrib.auth.models import User

class Specialist(models.Model):
    DESIGNER = 'Designer'
    MEASURER = 'Measurer'
    CONSULTANT = 'Consultant'
    SPECIALIST_TYPES = [
        (DESIGNER, 'Дизайнер'),
        (MEASURER, 'Замерщик'),
        (CONSULTANT, 'Консультант'),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    specialist_type = models.CharField(max_length=10, choices=SPECIALIST_TYPES)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.specialist_type})"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} {self.time} with {self.specialist}"