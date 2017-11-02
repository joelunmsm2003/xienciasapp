# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class EstAnx(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    descripcion = models.TextField(db_column='Descripcion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Est_Anx'


class EstLlam(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    descripcion = models.TextField(db_column='Descripcion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Est_Llam'


class MAnexos(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    n_anexo = models.IntegerField(db_column='N_Anexo', blank=True, null=True)  # Field name made lowercase.
    tipo = models.ForeignKey('Tipo', db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    fecha_hora = models.DateTimeField(db_column='Fecha-Hora', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    origen = models.IntegerField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    destino = models.IntegerField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    duracion = models.TimeField(db_column='Duracion', blank=True, null=True)  # Field name made lowercase.
    estado = models.ForeignKey(EstAnx, db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    ip_anexo = models.CharField(db_column='IP_Anexo', max_length=15, blank=True)  # Field name made lowercase.
    ip_servidor = models.IntegerField(db_column='IP_Servidor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M_Anexos'


class MErrores(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    descripcion = models.TextField(db_column='Descripcion', blank=True)  # Field name made lowercase.
    fecha_hora = models.DateTimeField(db_column='Fecha-Hora', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    flag = models.IntegerField(db_column='Flag', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M_Errores'


class MLlamadas(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    estado = models.ForeignKey(EstLlam, db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    tipo = models.ForeignKey('Tipo', db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    ip_servidor = models.CharField(db_column='IP_Servidor', max_length=15, blank=True)  # Field name made lowercase.
    datetime = models.DateTimeField(db_column='DateTime', blank=True, null=True)  # Field name made lowercase.
    origen = models.IntegerField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    destino = models.IntegerField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M_Llamadas'


class Tipo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    nametipo = models.TextField(db_column='NameTipo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tipo'


class Audios(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    audio1 = models.CharField(max_length=100, blank=True)
    audio2 = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'audios'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    databases = models.ForeignKey('Databases', db_column='databases')

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class Base(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    lote = models.ForeignKey('Lote', db_column='lote')

    class Meta:
        managed = False
        db_table = 'base'


class DBlaster(models.Model):
    id_d_blaster = models.IntegerField(primary_key=True)
    cliente = models.CharField(max_length=45, blank=True)
    uid = models.CharField(db_column='UID', max_length=45, blank=True)  # Field name made lowercase.
    fh_inicio = models.DateTimeField(db_column='FH_inicio', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(max_length=20, blank=True)
    audio = models.CharField(max_length=200, blank=True)
    derivacion = models.CharField(max_length=200, blank=True)
    lestado = models.ForeignKey('Estado', db_column='lEstado', blank=True, null=True)  # Field name made lowercase.
    respuesta = models.IntegerField(blank=True, null=True)
    dtmf = models.IntegerField(blank=True, null=True)
    despedida = models.IntegerField(blank=True, null=True)
    oc7_1 = models.IntegerField(db_column='OC7_1', blank=True, null=True)  # Field name made lowercase.
    oc7_2 = models.IntegerField(db_column='OC7_2', blank=True, null=True)  # Field name made lowercase.
    oc7_3 = models.CharField(db_column='OC7_3', max_length=10, blank=True)  # Field name made lowercase.
    tduracion_ini = models.DateTimeField(db_column='tDuracion_ini', blank=True, null=True)  # Field name made lowercase.
    tduracion_fin = models.DateTimeField(db_column='tDuracion_fin', blank=True, null=True)  # Field name made lowercase.
    tduracion = models.IntegerField(db_column='tDuracion', blank=True, null=True)  # Field name made lowercase.
    lote = models.CharField(max_length=100, blank=True)
    tipo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_blaster'


class DLlamadas(models.Model):
    id_d_llamadas = models.IntegerField(primary_key=True)
    id_d_blaster = models.IntegerField()
    cliente = models.CharField(max_length=45, blank=True)
    uid = models.CharField(db_column='UID', max_length=45, blank=True)  # Field name made lowercase.
    destino = models.CharField(max_length=20, blank=True)
    audio = models.CharField(max_length=200, blank=True)
    derivacion = models.CharField(max_length=200, blank=True)
    dtmf = models.IntegerField()
    despedida = models.IntegerField()
    llam_flag = models.IntegerField(blank=True, null=True)
    llam_uniqueid = models.CharField(max_length=45, blank=True)
    llam_tipo = models.IntegerField(blank=True, null=True)
    llam_canal = models.CharField(max_length=100, blank=True)
    llam_estado = models.IntegerField(blank=True, null=True)
    flagfin = models.IntegerField(db_column='flagFIN', blank=True, null=True)  # Field name made lowercase.
    t_ins = models.DateTimeField(db_column='T_INS')  # Field name made lowercase.
    t_pro = models.DateTimeField(db_column='T_PRO')  # Field name made lowercase.
    t_res = models.DateTimeField(db_column='T_RES')  # Field name made lowercase.
    t_fin1 = models.DateTimeField(db_column='T_FIN1')  # Field name made lowercase.
    t_fin2 = models.DateTimeField(db_column='T_FIN2')  # Field name made lowercase.
    d_timbrado = models.IntegerField()
    d_ivr = models.IntegerField()
    d_respuesta = models.IntegerField()
    d_total = models.IntegerField()
    respuesta01 = models.IntegerField(db_column='Respuesta01')  # Field name made lowercase.
    respuesta02 = models.IntegerField(db_column='Respuesta02')  # Field name made lowercase.
    codcorte = models.IntegerField(db_column='CodCorte')  # Field name made lowercase.
    vuelta = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'd_llamadas'


class Databases(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'databases'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Estado(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    nombre = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'estado'


class Excell(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    file = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'excell'


class Lote(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    aprobar = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lote'


class Servicio(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'servicio'


class Serviciouser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    servicio = models.ForeignKey(Servicio, db_column='servicio')
    user = models.ForeignKey(AuthUser, db_column='user')
    status = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'serviciouser'
