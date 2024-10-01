from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=1000)
    usn = models.CharField(max_length=10, unique=True, db_index= True)
    branch = models.CharField(max_length=10, null = True, blank=True)
   
    def __str__(self) -> str:
        return self.name

class Semester(models.Model):
    semester = models.PositiveSmallIntegerField( primary_key = True)

    def __str__(self) -> str:
        return f"{self.semester}"


class Subject(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=1000)
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE)
    credits = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

class VTUResult(models.Model):
    title = models.CharField(max_length=1000)
    code = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

class Result(models.Model):
    vturesult = models.ForeignKey(VTUResult, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internal = models.CharField(max_length=10)
    external = models.CharField(max_length=10)
    total = models.CharField(max_length=10)
    result = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.student} - {self.result}"

    class Meta:
        unique_together = ('student', 'vturesult', 'subject')

    
class SGPA(models.Model):
    result = models.ForeignKey(VTUResult, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sgpa = models.FloatField(null = True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
