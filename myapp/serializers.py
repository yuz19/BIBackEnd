from rest_framework import serializers
from .models import (
    AuthGroup,
    AuthGroupPermissions,
    AuthPermission,
    AuthUser,
    AuthUserGroups,
    AuthUserUserPermissions,
    Client,
    DjangoAdminLog,
    DjangoContentType,
    DjangoMigrations,
    DjangoSession,
    Expedition,
    Localisation,
    Produit,
    Retour,
    Time,
    TypeExpedition,
    Ventes,
)

class AuthGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthGroup
        fields = ['id', 'name']

class AuthGroupPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthGroupPermissions
        fields = ['id', 'group', 'permission']

class AuthPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthPermission
        fields = ['id', 'name', 'content_type', 'codename']

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']

class AuthUserGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserGroups
        fields = ['id', 'user', 'group']

class AuthUserUserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserUserPermissions
        fields = ['id', 'user', 'permission']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id', 'nom_client', 'categorie_client']

class DjangoAdminLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoAdminLog
        fields = ['id', 'action_time', 'object_id', 'object_repr', 'action_flag', 'change_message', 'content_type', 'user']

class DjangoContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoContentType
        fields = ['id', 'app_label', 'model']

class DjangoMigrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoMigrations
        fields = ['id', 'app', 'name', 'applied']

class DjangoSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoSession
        fields = ['session_key', 'session_data', 'expire_date']

class ExpeditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expedition
        fields = ['ville', 'date', 'client', 'expedition', 'produit_id', 'cout_expedition']

class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = ['ville_id', 'ville', 'etat', 'pays', 'code_postal', 'marche', 'region']

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['produit_id', 'category', 'sous_category', 'nom_produit', 'produit_priority']

class RetourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retour
        fields = ['date', 'client', 'produit', 'retour_quantity']

class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ['date_id', 'date', 'jour', 'mois', 'annee']

class TypeExpeditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeExpedition
        fields = ['expedition_id', 'mode_expidition']

class VentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventes
        fields = ['date', 'client', 'produit', 'ville', 'prix_ventes', 'quantity', 'reduction', 'profit']

