from django.urls import path
from . import views
from .views import movies_api
from movies.views import home, login_view

urlpatterns = [
    path("", views.home, name="movies_home"),
    path('content/', views.recommend_movie),
    path('top/', views.top_movies),
    path('user/<int:user_id>/', views.user_recommendation),
    path("api/movies/", movies_api, name="movies_api"),
    path("login/", login_view, name="login"),

]
