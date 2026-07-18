from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('expedition/<int:pk>/', views.ExpeditionDetailView.as_view(), name='expedition_detail'),
    path('destination/<int:pk>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('journal/', views.JournalView.as_view(), name='journal'),
    path('journal/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('checkout/<int:pk>/', views.CheckoutView.as_view(), name='checkout'),
    path('quick-booking/', views.QuickBookingView.as_view(), name='quick_booking'),
    path('add-review/', views.AddReviewView.as_view(), name='add_review'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
