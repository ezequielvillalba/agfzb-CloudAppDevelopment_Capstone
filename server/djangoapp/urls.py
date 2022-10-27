from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    
    path(route='', view=views.get_dealerships, name='index'),

    # path for about view
    path(route='about', view=views.about, name='about'),

    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    # path for registration
    path('registration/', views.registration_request, name='registration'),

    # path for login
    path('login/', views.login_request, name='login'),
    
    # path for logout
    path('logout/', views.logout_request, name='logout'),

    # path for add a review view
    path('dealer_review/<int:dealer_id>/', views.add_review, name='add_review'),
    
        # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),  
    path(route='dealer/<str:dealer_id>/', view=views.get_dealer_details, name='get_dealer_details'),
    path(route='<int:dealerId>/', view=views.get_dealerships_by_id, name='get_dealers_by_id'),
    path(route='<str:st>/', view=views.get_dealerships_by_state, name='get_dealers_by_state'),

    # path for add a review view
    path('dealer/<int:dealer_id>/add_review', views.add_review, name='add_review'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
