from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = 'ts_training'
urlpatterns = [

	# Authentication

	# /login
	path('login/', views.NTLoginView.as_view(), name='Login'),
	# /logout
	path('logout/', views.NTLogoutView.as_view(), name='Logout'),
	# /user
	path('user/done/', views.NTUserEditDone.as_view(), name='UserEditDone'),
	path('user/', views.NTUserEdit.as_view(), name='UserEdit'),

	# /
	path('', views.HomeView.as_view(), name="Home"),

	# People Views
	# /people
	path('people/', views.PeopleView.as_view(), name='People'),
	# /people/slug
	path('people/<slug:slug>/', views.PersonView.as_view(), name='Person'),
	
	# Training Spec Views
	# /training
	path('training/', views.TrainingView.as_view(), name='Category'),
	# /training/id
	path('training/<int:pk>/', views.TrainingDetailView.as_view(), name='TrainingDetail'),

	# Training Session Views
	# /training/session (List view)
	path('training/session', views.SessionView.as_view(), name='Sessions'),
	# /training/session/id (Single view)
	path('training/session/<int:pk>/', views.SessionSingleView.as_view(), name='SessionSingle'),

	#  Login required (handled in views.py)
	# /training/session/new (Create view)
#	url(r'^training/session/new/$', views.SessionNewView.as_view(), name='ntSessionNew'),
	# /training/session/id/edit (Update view)
	path('training/session/<int:pk>/edit/', views.SessionEditView.as_view(), name='SessionEdit'),

	# /training/plan (List view)
	path('training/plan/', views.PlanView.as_view(), name='Plan'),
	# /training/plan/id (single View)
	path('training/plan/<int:pk>/', views.PlanSingleView.as_view(), name='PlanSingle'),

	# /training/plan/new
	path('training/plan/new/', views.PlanNewView.as_view(), name='PlanNew'),
	# /training/plan/id/edit
	path('training/plan/<int:pk>/edit/', views.PlanEditView.as_view(), name='PlanEdit'),

	# /training/plan/signup
	path('training/plan/signup/<int:pk>/', views.SignupView.as_view(), name='Signup'),

	# About Page 
	# /about
	path('about/', views.AboutView.as_view(), name='About'),

	path('training/plan/complete/<int:pk>/', views.CreateSessionView, name="CreateSession"),

]
handler404 = views.PageNotFoundView.as_view()
