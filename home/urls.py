from django.urls import path, include
from home.views import Add_User,Get_All_Student,Get_All_Teacher,Update_Student,Update_Teacher,Delete_Student,Delete_Teacher,Assign_Student_Teacher

urlpatterns = [
    path("add_user",Add_User.as_view()),
    path("get_all_student",Get_All_Student.as_view()),
    path("get_all_teacher",Get_All_Teacher.as_view()),
    path("update_student",Update_Student.as_view()),
    path("update_teacher",Update_Teacher.as_view()),
    path("delete_student",Delete_Student.as_view()),
    path("delete_teacher",Delete_Teacher.as_view()),
    path("assign_student_teacher",Assign_Student_Teacher.as_view()),
]