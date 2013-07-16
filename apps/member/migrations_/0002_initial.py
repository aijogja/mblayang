# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profil'
        db.create_table('member_profil', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('nama', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('alamat', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tgl_lahir', self.gf('django.db.models.fields.DateField')(null=True)),
            ('propinsi', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wisata.Propinsi'], null=True, blank=True)),
            ('kota', self.gf('smart_selects.db_fields.ChainedForeignKey')(to=orm['wisata.Kota'], null=True, blank=True)),
            ('no_hape', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='L', max_length=2)),
            ('foto', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('member', ['Profil'])


    def backwards(self, orm):
        # Deleting model 'Profil'
        db.delete_table('member_profil')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'member.profil': {
            'Meta': {'object_name': 'Profil'},
            'alamat': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'foto': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'L'", 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kota': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['wisata.Kota']", 'null': 'True', 'blank': 'True'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'no_hape': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'propinsi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wisata.Propinsi']", 'null': 'True', 'blank': 'True'}),
            'tgl_lahir': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'wisata.kota': {
            'Meta': {'object_name': 'Kota'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nama_kota': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'propinsi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wisata.Propinsi']"})
        },
        'wisata.propinsi': {
            'Meta': {'object_name': 'Propinsi'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nama_propinsi': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ordinat': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['member']