from django.conf.urls import include, url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^teacher-list/$', views.TeacherListView.as_view(), name='teacher_list'),
    url(r'^subject-list/$', views.SubjectListView.as_view(), name='subject_list'),
    url(r'^school-class-detail/(?P<pk>[^/]*)/$', views.SchoolClassDetailView.as_view(), name='school_class_detail'),
    url(r'^teacher-students/(?P<slug>[^/]*)/$', views.TeacherStudentsView.as_view(), name='teacher_students'),
    url(r'^teacher-grade-students/(?P<slug>[^/]*)/(?P<grade>[^/]*)/$', views.TeacherGradeStudentsView.as_view(), name='teacher_grade_students'),
    url(r'^teacher-grade-students-by-class/(?P<slug>[^/]*)/(?P<grade>[^/]*)/$', views.TeacherGradeStudentsByClassView.as_view(), name='teacher_grade_students_by_class'),
    url(r'^subject-students/(?P<slug>[^/]*)/$', views.SubjectStudentsView.as_view(), name='subject_students'),
    url(r'^subject-students-by-teacher/(?P<slug>[^/]*)/$', views.SubjectStudentsByTeacherView.as_view(), name='subject_students_by_teacher'),
    url(r'^subject-students-by-class/(?P<slug>[^/]*)/$', views.SubjectStudentsByClassView.as_view(), name='subject_students_by_class'),
]
