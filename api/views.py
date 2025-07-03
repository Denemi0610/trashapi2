from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Utilisateur
from .serializers import UtilisateurSerializer, TokenObtainParTelephoneSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DemandeVidage, DemandeLavage, DemandePuisage
from .serializers import DemandeVidageSerializer, DemandeLavageSerializer, DemandePuisageSerializer


class InscriptionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur inscrit avec succès"})
        return Response(serializer.errors, status=400)

class ConnexionView(TokenObtainPairView):
    serializer_class = TokenObtainParTelephoneSerializer
   
#viewset pour utilisateur   
 
class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [IsAdminUser]

# viewset pour les demandes
class DemandeVidageViewSet(viewsets.ModelViewSet):
    serializer_class = DemandeVidageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.type_utilisateur == 'admin':
            return DemandeVidage.objects.all()
        return DemandeVidage.objects.filter(utilisateur=user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

class DemandeLavageViewSet(viewsets.ModelViewSet):
    serializer_class = DemandeLavageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.type_utilisateur == 'admin':
            return DemandeLavage.objects.all()
        return DemandeLavage.objects.filter(utilisateur=user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

class DemandePuisageViewSet(viewsets.ModelViewSet):
    serializer_class = DemandePuisageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.type_utilisateur == 'admin':
            return DemandePuisage.objects.all()
        return DemandePuisage.objects.filter(utilisateur=user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)
