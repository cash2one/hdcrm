from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import TemplateView



from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

urlpatterns = [
	url(r'^success',TemplateView.as_view(template_name="statics/success.html")),
	url(r'^error',TemplateView.as_view(template_name="statics/error.html")),
	url(r'^help',TemplateView.as_view(template_name="statics/help.html")),
	

	]
