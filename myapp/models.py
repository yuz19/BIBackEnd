# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Client(models.Model):
    client_id = models.CharField(db_column='client_ID', primary_key=True, max_length=256)  # Field name made lowercase.
    nom_client = models.CharField(max_length=256, blank=True, null=True)
    categorie_client = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client'


class Expedition(models.Model):
    ville = models.OneToOneField('Localisation', models.DO_NOTHING, db_column='ville_ID', primary_key=True)  # Field name made lowercase. The composite primary key (ville_ID, date_ID, expedition_ID, produit_id) found, that is not supported. The first column is selected.
    date = models.ForeignKey('Time', models.DO_NOTHING, db_column='date_ID')  # Field name made lowercase.
    client = models.ForeignKey(Client, models.DO_NOTHING, db_column='client_ID', blank=True, null=True)  # Field name made lowercase.
    expedition = models.ForeignKey('TypeExpedition', models.DO_NOTHING, db_column='expedition_ID')  # Field name made lowercase.
    produit_id = models.CharField(max_length=200)
    cout_expedition = models.IntegerField(db_column='cout_Expedition', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expedition'
        unique_together = (('ville', 'date', 'expedition', 'produit_id'),)


class Localisation(models.Model):
    ville_id = models.IntegerField(db_column='ville_ID', primary_key=True)  # Field name made lowercase.
    ville = models.CharField(max_length=256, blank=True, null=True)
    etat = models.CharField(max_length=256, blank=True, null=True)
    pays = models.CharField(max_length=256, blank=True, null=True)
    code_postal = models.CharField(max_length=256, blank=True, null=True)
    marche = models.CharField(max_length=256, blank=True, null=True)
    region = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localisation'


class Produit(models.Model):
    produit_id = models.CharField(primary_key=True, max_length=256)
    category = models.CharField(db_column='Category', max_length=256, blank=True, null=True)  # Field name made lowercase.
    sous_category = models.CharField(db_column='sous_Category', max_length=256, blank=True, null=True)  # Field name made lowercase.
    nom_produit = models.CharField(max_length=256, blank=True, null=True)
    produit_priority = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produit'


class Retour(models.Model):
    date = models.OneToOneField('Time', models.DO_NOTHING, db_column='date_ID', primary_key=True)  # Field name made lowercase. The composite primary key (date_ID, client_ID, produit_ID) found, that is not supported. The first column is selected.
    client = models.ForeignKey(Client, models.DO_NOTHING, db_column='client_ID')  # Field name made lowercase.
    produit = models.ForeignKey(Produit, models.DO_NOTHING, db_column='produit_ID')  # Field name made lowercase.
    retour_quantity = models.IntegerField(db_column='retour_Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'retour'
        unique_together = (('date', 'client', 'produit'),)


class Time(models.Model):
    date_id = models.CharField(db_column='date_ID', primary_key=True, max_length=512)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    jour = models.IntegerField(blank=True, null=True)
    mois = models.IntegerField(blank=True, null=True)
    annee = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time'


class TypeExpedition(models.Model):
    expedition_id = models.CharField(db_column='expedition_ID', primary_key=True, max_length=256)  # Field name made lowercase.
    mode_expidition = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_expedition'


class Ventes(models.Model):
    date = models.OneToOneField(Time, models.DO_NOTHING, db_column='date_ID', primary_key=True)  # Field name made lowercase. The composite primary key (date_ID, client_ID, produit_id, ville_ID) found, that is not supported. The first column is selected.
    client = models.ForeignKey(Client, models.DO_NOTHING, db_column='client_ID')  # Field name made lowercase.
    produit = models.ForeignKey(Produit, models.DO_NOTHING)
    ville = models.ForeignKey(Localisation, models.DO_NOTHING, db_column='ville_ID')  # Field name made lowercase.
    prix_ventes = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    reduction = models.IntegerField(blank=True, null=True)
    profit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ventes'
        unique_together = (('date', 'client', 'produit', 'ville'),)
