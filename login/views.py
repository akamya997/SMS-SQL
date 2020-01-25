from django.shortcuts import render,redirect
from . import models
from . import forms
from .table import *
from django_tables2 import RequestConfig

# 宏观部分
def index(request):
    return render(request,'login/index.html')


def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = 'please check again'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                userstu = models.Student.objects.get(xh=username)
                if userstu.password == password:
                    request.session['is_login'] = True
                    request.session['id'] = username
                    request.session['student'] = True
                    return redirect('/index/')
                else :
                    message = 'wrong password!'
            except:
                try:
                    usertea = models.Teacher.objects.get(gh=username)
                    if usertea.password == password:
                        request.session['is_login'] = True
                        request.session['id'] = username
                        request.session['teacher'] = True
                        return redirect('/index/')
                    else :
                        message = 'wrong password!'
                except:
                    message = "用户名不存在"
        return render(request, 'login/login.html',locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    pass
    return render(request,'login/register.html')


def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
    return redirect('/index/')


# 选课
def select(request):
    if request.session.get('student', None):
        if request.method == 'POST':
            pks = request.POST.getlist("selection")
            selected_objects = models.OpenCourse.objects.filter(pk__in=pks)
            res = []
            for u in selected_objects:
                cur = {'xh':request.session['id'], 'xq': u.xq, 'kh': u.lesson.kh, 'gh':u.teacher.gh}
                print(cur)
                try:
                    newRecord = models.Event(student=models.Student.objects.get(xh=cur['xh']),
                                             lesson=u, teacher=u.teacher)
                    newRecord.save()
                    cur['res'] = '选课成功'
                except:
                    cur['res'] = '已选此课'
                res.append(cur)
            message = SelectRes(res)
        all_course = models.OpenCourse.objects.all()
        course_data = []
        for u in all_course:
            cur = { 'pk': u.pk,
                    'kh': u.lesson.kh,
                   'km': u.lesson.km,
                   'teacher': u.teacher.xm,
                   'sksj': u.sksj,
                   'xq': u.xq}
            course_data.append(cur)
        table = SelectTable(course_data)
        return render(request, 'login/select.html', locals())
    else:
        return redirect('/index/')


# 退课
def drop_course(request):
    if request.session.get('student', None):
        if request.method == 'POST':
            res = []
            pks = request.POST.getlist("selection")
            selected_objects = models.Event.objects.filter(pk__in=pks)
            for u in selected_objects:
                cur = {'kh': u.lesson.lesson.kh, 'gh': u.teacher.gh, 'xq': u.lesson.xq}
                try:
                    u.delete()
                    cur['res'] = '退课成功'
                except:
                    cur['res'] = '退课失败'
                res.append(cur)
            print(res)
            message = SelectRes(res)
        table = EventTable(models.Event.objects.filter(student__xh=request.session['id']))
        return render(request, 'login/drop_course.html', locals())
    return redirect('/index')


# 查分
def score_query(request):
    if request.session.get('student', None):
        score_data = []
        selected_object = models.Event.objects.filter(student__xh=request.session['id'])
        for item in selected_object:
            cur = {'kh': item.lesson.lesson.kh,
                   'km': item.lesson.lesson.km,
                   'pscj': item.pscj,
                   'kscj': item.kscj,
                   'zpcj': item.zpcj}
            score_data.append(cur)
        table = ScoreTable(score_data)
        table.order_by = 'kh'
        return render(request, 'login/ScoreQuery.html',locals())
    return redirect('/index')


# 退学
def give_up(request):
    if request.session.get('student', None):
        tar = models.Student.objects.get(xh=request.session['id'])
        tar.delete()
        request.session.flush()
    return redirect('/index')


# 教师部分
def student_table(request):
    if request.session.get('teacher', None):
        table = StudentTable(models.Student.objects.all())
        return render(request, 'login/student_table.html', locals())
    return redirect('/index/')


def teacher_table(request):
    if request.session.get('teacher', None):
        table = TeacherTable(models.Teacher.objects.all())
        return render(request, 'login/teacher_table.html', locals())
    return redirect('/index/')


def course_table(request):
    if request.session.get('teacher', None):
        course_data = []
        selected_objects = models.OpenCourse.objects.filter(teacher__gh=request.session['id'])
        for u in selected_objects:
            cur = {'pk': u.pk,
                   'kh': u.lesson.kh,
                   'km': u.lesson.km,
                   'xq': u.xq,
                   'sksj': u.sksj}
            course_data.append(cur)
        table = CourseTable(course_data)
        return render(request, 'login/Course.html', locals())
    return redirect('/index/')


def open_course(request):
    if request.session.get('teacher', None):
        pass
    return redirect('/index/')


def input_score(request, pk):
    if request.session.get('teacher', None):
        current_kh = models.OpenCourse.objects.get(pk=pk).lesson.kh
        current_km = models.OpenCourse.objects.get(pk=pk).lesson.km
        tar = models.Event.objects.filter(lesson=models.OpenCourse.objects.get(pk=pk),
                                          teacher=models.Teacher.objects.get(gh=request.session['id']),
                                          zpcj__isnull=True).first()
        if request.method == 'POST':
            input_form = forms.InputForm(request.POST, instance=tar)
            print(print(input_form))
            if input_form.is_valid():
                input_form.save()
            tar = models.Event.objects.filter(lesson=models.OpenCourse.objects.get(pk=pk),
                                              teacher=models.Teacher.objects.get(gh=request.session['id']),
                                              zpcj__isnull=True).first()
        input_form = forms.InputForm(instance=tar)
        if not tar:
            message = 'All input has been done'
        return render(request, 'login/input_score.html', locals())
    return redirect('/index/')
