from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
	
urlpatterns = [
	path('', views.home, name = 'home'),
    path('register/', views.handle_registration, name = 'register'),
    path('login/', views.handle_login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('trips/', views.all_tripss, name = 'all_trips'),
    path('addtrip/', views.add_trip, name = 'add_trip'),
    path('likedTrips', views.likedTrips),
    path('addToLikedTrip/<int:tripId>', views.addToLikedTrip),
    path('delete/<int:tripId>', views.deleteTrip),
    path('remove/<int:tripId>', views.removeTrip),
    path('trips/<tripId>', views.view_trip, name = 'view_trip'),
    path('reviews/<int:tripId>', views.trip_reviews, name = 'trip_reviews'),
    # path('comments/<int:reviewId>', views.review_comments, name = 'review_comments'),
    path('postreview/', views.post_review, name = 'post_review'),
    path('postcomment/<int:reviewId>', views.post_comment, name = 'post_comment'),
    path('deletereview/<int:reviewId>', views.delete_review, name = 'delete_review'),
    path('deletecomment/<int:commentId>', views.delete_comment, name = 'delete_comment'),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)