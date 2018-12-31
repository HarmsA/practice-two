from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.login, name='login'),
    url(r'^login/$',views.login, name='login'),
    url(r'^process_register/$',views.process_register, name='process_register'),
    url(r'^process_login/$',views.process_login, name='process_login'),
    url(r'^logout/$',views.logout, name='logout'),
    url(r'^addjob/$',views.addjob, name='addjob'),
    url(r'^addjob_verify/$',views.addjob_verify, name='addjob_verify'),
    url(r'^update_job_verify/$',views.update_job_verify, name='update_job_verify'),
    url(r'^dashboard/$',views.dashboard, name='dashboard'),
    url(r'^create_job_for_user/(?P<job_id>\d+)/$',views.create_job_for_user, name='create_job_for_user'),
    url(r'^view_job/(?P<job_id>\d+)/$',views.view_job, name='view_job'),
    url(r'^edit_job/(?P<job_id>\d+)/$',views.edit_job, name='edit_job'),
    url(r'^delete/(?P<job_id>\d+)/$',views.delete, name='delete'),
]
