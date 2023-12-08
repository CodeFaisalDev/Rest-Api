from django.urls import path
# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import (WatchListAV, 
                                     WatchDetailAV, 
                                     StreamAV, 
                                     StreamDetailsAV, 
                                     ReviewAV, 
                                     ReviewDetailAV,
                                     ReviewCreateAV)
urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('list/<int:pk>', WatchDetailAV.as_view(), name='watchlist-detail'),


    path('stream/', StreamAV.as_view(), name='stream_list'),
    path('stream/<int:pk>', StreamDetailsAV.as_view(), name='stream-detail'),
    
    path('list/<int:pk>/review-create', ReviewCreateAV.as_view(), name='review-create'),
    path('list/<int:pk>/review', ReviewAV.as_view(), name='review-list'),
    path('stream/review/<int:pk>', ReviewDetailAV.as_view(), name='review-detail'),
]
