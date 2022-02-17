from django.urls import path
from . import views

app_name = 'Calendar'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='cal'),
    path('event/new/', views.event, name='event_new'),
	path('event/edit/(?P<event_id>\d+)', views.event, name='event_edit'),
]
