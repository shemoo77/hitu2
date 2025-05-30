from django.db import models
from django.contrib.auth.models import User
from structure.models import StudentStructure


class Student(models.Model):
    user =models.OneToOneField(User , on_delete=models.CASCADE , blank=True , null=True)
    name =models.CharField(max_length=25)
    mobile =models.CharField(max_length=11 , blank=True , null=True)
    national_id =models.CharField(max_length=14)
    structure = models.ForeignKey(StudentStructure, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__ (self):
        return (self.name)
    
    def get_my_courses(self):
        from courses.models import Course
        if self.structure:
            return Course.objects.filter(
                department=self.structure.department,
                academic_year=self.structure.year,
                semester=self.structure.semester
            )
        return Course.objects.none()

class Doctor(models.Model):
    user =models.OneToOneField(User , on_delete=models.CASCADE , blank=True , null=True)
    name =models.CharField(max_length=25)
    mobile =models.CharField(max_length=11 ,blank=True , null=True )
    national_id =models.CharField(max_length=14)
    structure = models.ManyToManyField('structure.StudentStructure', blank=True)
    is_admin_doctor = models.BooleanField(default=False)


    def __str__ (self):
        return (self.name)
    
    def get_my_courses(self):
        from courses.models import Course
        return Course.objects.filter(doctor=self)
    

