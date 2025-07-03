
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UtilisateurViewSet,
    DemandeVidageViewSet,
    DemandeLavageViewSet,
    DemandePuisageViewSet,
    InscriptionView,
    ConnexionView
)

router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')
router.register(r'demandes/vidage', DemandeVidageViewSet, basename='demande-vidage')
router.register(r'demandes/lavage', DemandeLavageViewSet, basename='demande-lavage')
router.register(r'demandes/puisage', DemandePuisageViewSet, basename='demande-puisage')

urlpatterns = [
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('connexion/', ConnexionView.as_view(), name='connexion'),
    path('', include(router.urls)),
]

