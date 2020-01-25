import django_tables2 as tables
from .models import Student,Teacher,OpenCourse,Event


class StudentTable(tables.Table):
    class Meta:
        model = Student
        template_name = 'django_tables2/bootstrap.html'
        fields = ('xh', 'xm', 'xb', 'csrq', 'jg', 'sjhm')
        attrs = {"class": "table table-bordered table-striped"}
        orderable = False


class TeacherTable(tables.Table):
    class Meta:
        model = Teacher
        template_name = 'django_tables2/bootstrap.html'
        fields = ('gh', 'xm', 'xb', 'csrq', 'xl', 'jbgz')
        attrs = {"class": "table table-bordered table-striped"}
        orderable = False


class SelectTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', attrs={"th__input":{"onclick":"toggle(this)"}})
    kh = tables.Column(verbose_name='课号')
    km = tables.Column(verbose_name='课名')
    teacher = tables.Column(verbose_name='教师')
    sksj = tables.Column(verbose_name='上课时间')
    xq = tables.Column(verbose_name='学期')

    class Meta:
        model = OpenCourse
        fields = ()
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-bordered table-striped"}
        orderable = False


class EventTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', attrs={"th__input": {"onclick": "toggle(this)"}})

    class Meta:
        model = Event
        exclude = ('id', 'pscj', 'zpcj', 'kscj')
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-bordered table-striped"}
        orderable = False
        sequence = ('selection', '...')


class SelectRes(tables.Table):
    kh = tables.Column(verbose_name='课号')
    gh = tables.Column(verbose_name='工号')
    xq = tables.Column(verbose_name='学期')
    res = tables.Column(verbose_name='结果')

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-bordered table-striped"}
        orderable = False


class ScoreTable(tables.Table):
    kh = tables.Column(verbose_name='课号')
    km = tables.Column(verbose_name='课名')
    pscj = tables.Column(verbose_name='平时成绩')
    kscj = tables.Column(verbose_name='考试成绩')
    zpcj = tables.Column(verbose_name='总评成绩')

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-bordered table-striped"}
        orderable = False


class CourseTable(tables.Table):
    kh = tables.Column(verbose_name='课号')
    km = tables.Column(verbose_name='课名')
    xq = tables.Column(verbose_name='学期')
    sksj = tables.Column(verbose_name='上课时间')
    edit = tables.TemplateColumn(
        template_code='<a class="btn btn-info btn-sm" href="{% url \'InputScore\' record.pk %}">录入</a>',
        verbose_name='成绩录入')

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-bordered table-striped"}
        orderable = False

