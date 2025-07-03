from rest_framework import serializers
from .models import Utilisateur, DemandeVidage, DemandeLavage, DemandePuisage
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'type_utilisateur', 'numero_tel', 'nom', 'prenom', 'ville', 'quartier', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        utilisateur = Utilisateur(**validated_data)
        utilisateur.set_password(password)
        utilisateur.save()
        return utilisateur

#connexion avec JWT

class TokenObtainParTelephoneSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        numero_tel = attrs.get("numero_tel")
        password = attrs.get("password")

        user = authenticate(numero_tel=numero_tel, password=password)
        if not user:
            raise serializers.ValidationError("Identifiants invalides.")

        refresh = self.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "numero_tel": user.numero_tel,
            "type_utilisateur": user.type_utilisateur,
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["numero_tel"] = user.numero_tel
        token["type_utilisateur"] = user.type_utilisateur
        return token
    

# 🔁 Fonction utilitaire
def make_statut_read_only_if_not_admin(self, instance, validated_data):
    user = self.context['request'].user
    if user.type_utilisateur != 'admin':
        validated_data.pop('statut', None)
    return validated_data

class DemandeVidageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeVidage
        fields = ['id', 'utilisateur', 'date_de_la_demande', 'statut']
        read_only_fields = ['utilisateur', 'date_de_la_demande']

    def update(self, instance, validated_data):
        validated_data = make_statut_read_only_if_not_admin(self, instance, validated_data)
        return super().update(instance, validated_data)

class DemandeLavageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeLavage
        fields = ['id', 'utilisateur', 'date_de_la_demande', 'statut']
        read_only_fields = ['utilisateur', 'date_de_la_demande']

    def update(self, instance, validated_data):
        validated_data = make_statut_read_only_if_not_admin(self, instance, validated_data)
        return super().update(instance, validated_data)

class DemandePuisageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandePuisage
        fields = ['id', 'utilisateur', 'date_de_la_demande', 'statut']
        read_only_fields = ['utilisateur', 'date_de_la_demande']

    def update(self, instance, validated_data):
        validated_data = make_statut_read_only_if_not_admin(self, instance, validated_data)
        return super().update(instance, validated_data)
