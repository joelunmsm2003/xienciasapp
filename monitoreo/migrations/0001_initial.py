# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audios',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('audio1', models.CharField(max_length=100, blank=True)),
                ('audio2', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'db_table': 'audios',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField()),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=75)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'base',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Databases',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'databases',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DBlaster',
            fields=[
                ('id_d_blaster', models.IntegerField(serialize=False, primary_key=True)),
                ('cliente', models.CharField(max_length=45, blank=True)),
                ('uid', models.CharField(max_length=45, db_column='UID', blank=True)),
                ('fh_inicio', models.DateTimeField(null=True, db_column='FH_inicio', blank=True)),
                ('destino', models.CharField(max_length=20, blank=True)),
                ('audio', models.CharField(max_length=200, blank=True)),
                ('derivacion', models.CharField(max_length=200, blank=True)),
                ('respuesta', models.IntegerField(null=True, blank=True)),
                ('dtmf', models.IntegerField(null=True, blank=True)),
                ('despedida', models.IntegerField(null=True, blank=True)),
                ('oc7_1', models.IntegerField(null=True, db_column='OC7_1', blank=True)),
                ('oc7_2', models.IntegerField(null=True, db_column='OC7_2', blank=True)),
                ('oc7_3', models.CharField(max_length=10, db_column='OC7_3', blank=True)),
                ('tduracion_ini', models.DateTimeField(null=True, db_column='tDuracion_ini', blank=True)),
                ('tduracion_fin', models.DateTimeField(null=True, db_column='tDuracion_fin', blank=True)),
                ('tduracion', models.IntegerField(null=True, db_column='tDuracion', blank=True)),
                ('lote', models.CharField(max_length=100, blank=True)),
                ('tipo', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'd_blaster',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.IntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DLlamadas',
            fields=[
                ('id_d_llamadas', models.IntegerField(serialize=False, primary_key=True)),
                ('id_d_blaster', models.IntegerField()),
                ('cliente', models.CharField(max_length=45, blank=True)),
                ('uid', models.CharField(max_length=45, db_column='UID', blank=True)),
                ('destino', models.CharField(max_length=20, blank=True)),
                ('audio', models.CharField(max_length=200, blank=True)),
                ('derivacion', models.CharField(max_length=200, blank=True)),
                ('dtmf', models.IntegerField()),
                ('despedida', models.IntegerField()),
                ('llam_flag', models.IntegerField(null=True, blank=True)),
                ('llam_uniqueid', models.CharField(max_length=45, blank=True)),
                ('llam_tipo', models.IntegerField(null=True, blank=True)),
                ('llam_canal', models.CharField(max_length=100, blank=True)),
                ('llam_estado', models.IntegerField(null=True, blank=True)),
                ('flagfin', models.IntegerField(null=True, db_column='flagFIN', blank=True)),
                ('t_ins', models.DateTimeField(db_column='T_INS')),
                ('t_pro', models.DateTimeField(db_column='T_PRO')),
                ('t_res', models.DateTimeField(db_column='T_RES')),
                ('t_fin1', models.DateTimeField(db_column='T_FIN1')),
                ('t_fin2', models.DateTimeField(db_column='T_FIN2')),
                ('d_timbrado', models.IntegerField()),
                ('d_ivr', models.IntegerField()),
                ('d_respuesta', models.IntegerField()),
                ('d_total', models.IntegerField()),
                ('respuesta01', models.IntegerField(db_column='Respuesta01')),
                ('respuesta02', models.IntegerField(db_column='Respuesta02')),
                ('codcorte', models.IntegerField(db_column='CodCorte')),
                ('vuelta', models.IntegerField()),
            ],
            options={
                'db_table': 'd_llamadas',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'db_table': 'estado',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstAnx',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('descripcion', models.TextField(db_column='Descripcion')),
            ],
            options={
                'db_table': 'Est_Anx',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstLlam',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('descripcion', models.TextField(db_column='Descripcion')),
            ],
            options={
                'db_table': 'Est_Llam',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Excell',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('file', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'db_table': 'excell',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField()),
                ('aprobar', models.IntegerField()),
            ],
            options={
                'db_table': 'lote',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MAnexos',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('n_anexo', models.IntegerField(null=True, db_column='N_Anexo', blank=True)),
                ('fecha_hora', models.DateTimeField(null=True, db_column='Fecha-Hora', blank=True)),
                ('origen', models.IntegerField(null=True, db_column='Origen', blank=True)),
                ('destino', models.IntegerField(null=True, db_column='Destino', blank=True)),
                ('duracion', models.TimeField(null=True, db_column='Duracion', blank=True)),
                ('ip_anexo', models.CharField(max_length=15, db_column='IP_Anexo', blank=True)),
                ('ip_servidor', models.IntegerField(null=True, db_column='IP_Servidor', blank=True)),
            ],
            options={
                'db_table': 'M_Anexos',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MErrores',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('descripcion', models.TextField(db_column='Descripcion', blank=True)),
                ('fecha_hora', models.DateTimeField(null=True, db_column='Fecha-Hora', blank=True)),
                ('flag', models.IntegerField(null=True, db_column='Flag', blank=True)),
            ],
            options={
                'db_table': 'M_Errores',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MLlamadas',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('ip_servidor', models.CharField(max_length=15, db_column='IP_Servidor', blank=True)),
                ('datetime', models.DateTimeField(null=True, db_column='DateTime', blank=True)),
                ('origen', models.IntegerField(null=True, db_column='Origen', blank=True)),
                ('destino', models.IntegerField(null=True, db_column='Destino', blank=True)),
            ],
            options={
                'db_table': 'M_Llamadas',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'servicio',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Serviciouser',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'db_table': 'serviciouser',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('nametipo', models.TextField(db_column='NameTipo')),
            ],
            options={
                'db_table': 'Tipo',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
