from django.db import models

class Department(models.Model):
    department_id = models.AutoField(primary_key=True, db_column='Department_ID')
    department_name = models.CharField(max_length=100, unique=True, db_column='Department_Name')
    description = models.TextField(blank=True, null=True, db_column='Description')

    class Meta:
        managed = False
        db_table = 'Departments'

    def __str__(self):
        return self.department_name

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    patient_id = models.AutoField(primary_key=True, db_column='Patient_ID')
    name = models.CharField(max_length=100, db_column='Name')
    age = models.IntegerField(blank=True, null=True, db_column='Age')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, db_column='Gender')
    email = models.CharField(max_length=100, unique=True, db_column='Email')
    phone = models.CharField(max_length=15, blank=True, null=True, db_column='Phone')
    address = models.TextField(blank=True, null=True, db_column='Address')
    password = models.CharField(max_length=255, db_column='Password')

    class Meta:
        managed = False
        db_table = 'Patients'

    def __str__(self):
        return self.name

class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True, db_column='Doctor_ID')
    department = models.ForeignKey(Department, models.DO_NOTHING, db_column='Department_ID', blank=True, null=True)
    name = models.CharField(max_length=100, db_column='Name')
    qualification = models.CharField(max_length=100, blank=True, null=True, db_column='Qualification')
    specialization = models.CharField(max_length=100, blank=True, null=True, db_column='Specialization')
    experience = models.IntegerField(blank=True, null=True, db_column='Experience')
    hospital = models.CharField(max_length=100, blank=True, null=True, db_column='Hospital')
    fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='Fees')
    available_days = models.CharField(max_length=100, blank=True, null=True, db_column='Available_Days')
    available_time = models.CharField(max_length=100, blank=True, null=True, db_column='Available_Time')
    email = models.CharField(max_length=100, unique=True, blank=True, null=True, db_column='Email')
    phone = models.CharField(max_length=15, blank=True, null=True, db_column='Phone')
    password = models.CharField(max_length=255, blank=True, null=True, db_column='Password')
    status = models.CharField(max_length=20, default='Active', db_column='Status')

    class Meta:
        managed = False
        db_table = 'Doctors'

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    appointment_id = models.AutoField(primary_key=True, db_column='Appointment_ID')
    patient = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_ID')
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='Doctor_ID')
    appointment_date = models.DateField(blank=True, null=True, db_column='Appointment_Date')
    appointment_time = models.TimeField(blank=True, null=True, db_column='Appointment_Time')
    reason = models.TextField(blank=True, null=True, db_column='Reason')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, null=True, db_column='Status')

    class Meta:
        managed = False
        db_table = 'Appointments'

class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True, db_column='Prescription_ID')
    appointment = models.ForeignKey(Appointment, models.DO_NOTHING, db_column='Appointment_ID')
    diagnosis = models.TextField(blank=True, null=True, db_column='Diagnosis')
    medicine = models.CharField(max_length=255, blank=True, null=True, db_column='Medicine')
    dosage = models.CharField(max_length=100, blank=True, null=True, db_column='Dosage')
    instructions = models.TextField(blank=True, null=True, db_column='Instructions')

    class Meta:
        managed = False
        db_table = 'Prescriptions'

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True, db_column='Admin_ID')
    username = models.CharField(unique=True, max_length=50, db_column='Username')
    email = models.CharField(unique=True, max_length=100, blank=True, null=True, db_column='Email')
    password = models.CharField(max_length=255, db_column='Password')

    class Meta:
        managed = False
        db_table = 'Admins'

    def __str__(self):
        return self.username

class Review(models.Model):
    review_id = models.AutoField(primary_key=True, db_column='Review_ID')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='Patient_ID')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='Doctor_ID')
    rating = models.IntegerField(db_column='Rating')
    comment = models.TextField(blank=True, null=True, db_column='Comment')
    created_at = models.DateTimeField(auto_now_add=True, db_column='Created_At')

    class Meta:
        db_table = 'Reviews'

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True, db_column='Notification_ID')
    user_type = models.CharField(max_length=20, db_column='User_Type')  # 'Admin', 'Doctor', 'Patient'
    user_id = models.IntegerField(db_column='User_ID')
    message = models.TextField(db_column='Message')
    is_read = models.BooleanField(default=False, db_column='Is_Read')
    created_at = models.DateTimeField(auto_now_add=True, db_column='Created_At')

    class Meta:
        db_table = 'Notifications'
