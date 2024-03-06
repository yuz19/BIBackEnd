from rest_framework import serializers
from .models import (
    Client,
    Expedition,
    Localisation,
    Produit,
    Retour,
    Time,
    TypeExpedition,
    Ventes,
)

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id', 'nom_client', 'categorie_client']

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
