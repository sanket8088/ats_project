from django.db import models

class Candidate(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected')
    ]
    
    name = models.CharField(max_length=100, db_index=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    years_of_exp = models.IntegerField()
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
