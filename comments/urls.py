from django.urls import path
from comments.views import add_comment

app_name = "comments"


urlpatterns = [
    path('tweet/<uuid:pk>/comment/', add_comment, name='add-comment'),
    

]
