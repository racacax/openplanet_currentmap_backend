from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.RegisterView.as_view(), name='login'),
    path('groups_owned/', views.GroupsOwnedView.as_view(), name='groups_owned'),
    path('groups_joined/', views.GroupsJoinedView.as_view(), name='groups_joined'),
    path('sent_invites/', views.SentInvitesView.as_view(), name='sent_invites'),
    path('received_invites/', views.ReceivedInvitesView.as_view(), name='received_invites'),
    path('remove_player_from_group/', views.RemovePlayerView.as_view(), name='remove_player_from_group'),
    path('main_loop/', views.LoopView.as_view(), name='main_loop'),
    path('find_player/', views.FindPlayerView.as_view(), name='find_player'),
]

