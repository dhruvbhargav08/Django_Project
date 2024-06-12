from django.urls import path, include
from home.views import Add_User,Get_All_User,Get_User,Update_User,Delete_User

urlpatterns = [
    path("add_user",Add_User.as_view()),
    path("get_all_user",Get_All_User.as_view()),
    path("get_user",Get_User.as_view()),
    path("update_user",Update_User.as_view()),
    path("delete_user",Delete_User.as_view())
]