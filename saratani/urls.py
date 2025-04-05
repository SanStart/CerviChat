from django.urls import path
from . import views
urlpatterns = [
    path('', views.predictions, name="predictions"),
    path('predictions/<uuid:image_id>/', views.predict_paps, name="predict"),
    path('report/<uuid:ide>/', views.report, name="report"),
    path('delete/<uuid:ide>/', views.delete_prediction, name="delete-prediction"),
    path('analysis/<uuid:id>/', views.analysis, name='analysis')
]
