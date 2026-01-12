from django.urls import path
from .views import home, predict_insurance

urlpatterns = [
    path("", home, name="home"),   # page d’accueil
    path("predict/", predict_insurance, name="predict"),
]
