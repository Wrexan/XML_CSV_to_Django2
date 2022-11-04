from django.shortcuts import render
from django.views.generic import ListView
from users.models import User


class UserList(ListView):
    # model = User

    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        print(user_list)
        return render(request, "users/users.html", {"user_list": user_list})
