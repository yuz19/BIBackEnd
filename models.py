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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Localisation(models.Model):
    ville_id = models.IntegerField(db_column='ville_ID', primary_key=True)  # Field name made lowercase.
    ville = models.CharField(max_length=256, blank=True, null=True)
    etat = models.CharField(max_length=256, blank=True, null=True)
    pays = models.CharField(max_length=256, blank=True, null=True)
    code_postal = models.CharField(max_length=256, blank=True, null=True)
    marche = models.CharField(max_length=256, blank=True, null=True)
    region = models.CharField(db_column='Region', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'localisation'


class Produit(models.Model):
    produit_id = models.CharField(primary_key=True, max_length=512)
    category = models.CharField(db_column='Category', max_length=512, blank=True, null=True)  # Field name made lowercase.
    sous_category = models.CharField(db_column='sous_Category', max_length=512, blank=True, null=True)  # Field name made lowercase.
    nom_produit = models.CharField(max_length=512, blank=True, null=True)
    produit_priority = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produit'


class Time(models.Model):
    date_id = models.CharField(db_column='date_ID', primary_key=True, max_length=200)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    annee = models.IntegerField(blank=True, null=True)
    mois = models.IntegerField(blank=True, null=True)
    jour = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time'


class TypeExpedition(models.Model):
    expedition_id = models.CharField(db_column='expedition_ID', max_length=256, blank=True, null=True)  # Field name made lowercase.
    mode_expidition = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_expedition'
