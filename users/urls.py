import users.views

urlpatterns = ('/', users.views.UserList.as_view())
