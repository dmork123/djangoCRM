from django.urls import path
from .views import (
    LeadListView, 
    lead_detail, 
    lead_create, 
    lead_update, 
    lead_delete, 
    LeadDetailView, 
    LeadCreateView, 
    LeadUpdateView, 
    LeadDeleteView, 
    SignupView,
    AssignAgentView,
    CategoryListView
)

app_name = "leads"  

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name="assign-agent"),
    path('categories/', CategoryListView.as_view(), name='category-list'),

]
