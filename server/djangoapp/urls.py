from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='dealer/<str:dealer_id>/', view=views.get_dealer_details, name='get_dealer_details'),
    path('dealer_review/<int:dealer_id>/', views.add_review, name='add_review'),
    # path('review_post/<int:dealer_id>/', views.post_review, name='post_review'),
    path(route='<int:dealerId>/', view=views.get_dealerships_by_id, name='get_dealers_by_id'),
    path(route='dealer_state_abbr/', view=views.get_dealerships_by_state_abbr, name='get_dealers_by_state_abbr'),
    #path(route='<str:st>/', view=views.get_dealerships_by_state, name='get_dealers_by_state'),
    path(route="about/", view=views.about, name='about'),
    path(route="contact/", view=views.contact, name='contact'),
    path(route='', view=views.get_dealerships, name='index'),
    path(route='register/', view=views.registration_request, name='register'),
    # path for login
    path(route='login/', view=views.login_request, name='login'),
    # path for logout
    path(route='logout/', view=views.logout_request, name='logout'),    
    path(route='',view=views.get_dealerships, name='index'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
