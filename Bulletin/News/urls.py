from django.urls import path
from News import views

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('bulletin/',views.PostListView.as_view(),name='post_list'),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),
    path('contact/',views.ContactView.as_view(),name='contact'),
    path('subscription/',views.SubscriptionView.as_view(),name='subscription'),
    path('post/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
    path('post/new',views.CreatePostView.as_view(),name="post_new"),
    path('post/<int:pk>/edit/',views.PostUpdateView.as_view(),name="post_edit"),
    path('post/<int:pk>/remove/',views.PostDeleteView.as_view(),name="post_remove"),
    path('draft/',views.DraftListView.as_view(),name='draft_list'),
    path('post/<int:pk>/comment/',views.add_comment_to_post,name='add_comment_to_post'),
    path('comment/<int:pk>/approve/',views.comment_approve,name='comment_approve'),
    path('comment/<int:pk>/remove/',views.comment_remove,name='comment_remove'),
    path('post/<int:pk>/publish/',views.post_publish,name='post_publish'),
    path('notes/', views.NotesView.as_view(), name='notes'),
]
