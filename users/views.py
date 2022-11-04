from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from .models import User
from .forms import FileFieldForm


class UserList(ListView):
    # model = User

    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        return render(request, "users/users.html", {"user_list": user_list,
                                                    "a_user_list": "active"})


class UserUploadFormView(FormView):
    form_class = FileFieldForm
    template_name = 'users/upload_users.html'
    success_url = "/"

    def get(self, request, *args, **kwargs):
        # if request.user.is_superuser:
        #     return render(request, self.template_name)
        # return redirect('/')

        return render(request, self.template_name, {"a_upload_users": "active"})

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            files = request.FILES.getlist('files')
            if form.is_valid():
                # uploader = UserUploader()
                # uploader.handle_uploaded_files(request, files)
                return super().form_valid(form)
            else:
                return self.form_invalid(form)
        return redirect('/')


