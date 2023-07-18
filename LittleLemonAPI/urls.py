from django.urls import path
from . import views

urlpatterns = [
    # path("menu-items", views.MenuItemsView.as_view()),
    # path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
    path("menu-items", views.MenuItemsViewSet.as_view({
        'get': 'list',
        "post": "create"
    })),
    path("menu-items/<int:pk>", views.MenuItemsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path("category", views.CategoryViewSet.as_view({
        'get': 'list',
        "post": "create"
    })),
    path("category/<int:pk>", views.CategoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('groups/manager/users/', views.GroupViewSet.as_view({
        'get': 'list', 
        'post': 'create', 
        'delete': 'destroy'
    })),
    # path('groups/manager/users/<int:pk>/', views.ManagerUserDetailView.as_view(), name='manager-user-detail'),
    path('groups/delivery-crew/users/', views.DeliveryCrewViewSet.as_view({
        'get': 'list', 
        'post': 'create', 
        'delete': 'destroy'
    })),
    # path('groups/delivery-crew/users/<int:pk>/', views.DeliveryCrewUserDetailView.as_view(), name='delivery-crew-user-detail'),
    path('orders/', views.OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('cart/menu-items', views.CartView.as_view()),
]
