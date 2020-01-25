from django.db import models


class Department(models.Model):
    yxh = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.yxh

class Student(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    xh = models.CharField(max_length=128, unique=True, verbose_name='学号')
    password = models.CharField(max_length=128)
    xm = models.CharField(max_length=128, verbose_name='姓名')
    xb = models.CharField(max_length=32, choices=gender, default="男", verbose_name='性别')
    csrq = models.CharField(max_length=128, null=True, verbose_name='出生日期')
    jg = models.CharField(max_length=128, null=True, verbose_name='籍贯')
    sjhm = models.CharField(max_length=128, null=True, verbose_name='手机号码')
    depart = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='院系号')

    def __str__(self):
        return self.xm

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生"


class Teacher(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    gh = models.CharField(max_length=128, unique=True, verbose_name='工号')
    password = models.CharField(max_length=128)
    xm = models.CharField(max_length=128, verbose_name='姓名')
    xb = models.CharField(max_length=32, choices=gender, default="男", verbose_name='性别')
    csrq = models.CharField(max_length=128, null=True, verbose_name='出生日期')
    xl = models.CharField(max_length=128, null=True, verbose_name='学历')
    jbgz = models.IntegerField(verbose_name='基本工资')
    depart = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.xm

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = "教师"


class Course(models.Model):
    kh = models.CharField(max_length=128, unique=True, verbose_name='课号')
    km = models.CharField(max_length=128, verbose_name='课名')
    xf = models.IntegerField(verbose_name='学分')
    xs = models.IntegerField(verbose_name='学时')
    depart = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='院系号')

    def __str__(self):
        return self.kh

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = "课程"


class OpenCourse(models.Model):
    xq = models.CharField(max_length=128, verbose_name='学期')
    lesson = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, verbose_name='教师', on_delete=models.CASCADE)
    sksj = models.CharField(max_length=128, verbose_name='上课时间')

    def __str__(self):
        return str(self.xq) + ' ' + str(self.lesson)

    class Meta:
        unique_together = ('xq', 'lesson', 'teacher')
        verbose_name = '开课'
        verbose_name_plural = '开课'


class Event(models.Model):
    student = models.ForeignKey(Student, verbose_name='姓名', on_delete=models.CASCADE)
    lesson = models.ForeignKey(OpenCourse, verbose_name='课程', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, verbose_name='教师', on_delete=models.CASCADE)
    pscj = models.IntegerField(verbose_name='平时成绩', null=True)
    kscj = models.IntegerField(verbose_name='考试成绩', null=True)
    zpcj = models.IntegerField(verbose_name='总评成绩', null=True)

    class Meta:
        unique_together = ('student', 'lesson', 'teacher')
        verbose_name = '选课'
        verbose_name_plural = '选课'
