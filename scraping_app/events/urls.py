from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('search_history.html', views.search_history),
    path('search.html', views.search,name='search'),
    path('history.html',views.history,name="history"),
    path('show_history/<history_id>',views.show_history,name="show_history"),
    path('history_csv',views.history_csv,name="history_csv"),
   
]
