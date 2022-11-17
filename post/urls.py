from django.urls import path

from post.views.API.post import *
from post.views.API.like import *
from post.views.API.comment import *

urlpatterns = [

    path('', PostListCreateAPIView.as_view(), name='post_view'),
    path('<int:pk>', PostRetrieveUpdateDestroyAPIViewAPIView.as_view(), name='get_post'),
    
    path('search', SearchPeopleAPIViewAPIView.as_view(), name='search_people'),
    path('newsfeed', AllPostAPIViewAPIView.as_view(), name='newsfeed'),

    path('comments', CommentListCreateAPIView.as_view(), name='post_view'),
    path('comments/<int:pk>', CommentRetrieveUpdateDestroyAPIViewAPIView.as_view(), name='get_post'),

    path('likes', LikeListCreateAPIView.as_view(), name='post_view'),
    path('likes/<int:pk>', LikeRetrieveUpdateDestroyAPIViewAPIView.as_view(), name='get_post'),
]