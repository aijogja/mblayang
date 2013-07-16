# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Kategori'
        db.create_table('wisata_kategori', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kategori', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('wisata', ['Kategori'])

        # Adding model 'Propinsi'
        db.create_table('wisata_propinsi', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nama_propinsi', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('ordinat', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('wisata', ['Propinsi'])

        # Adding model 'Kota'
        db.create_table('wisata_kota', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('propinsi', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wisata.Propinsi'])),
            ('nama_kota', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('wisata', ['Kota'])

        # Adding model 'Wisata'
        db.create_table('wisata_wisata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nama', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('kategori', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wisata.Kategori'], null=True, blank=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('propinsi', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wisata.Propinsi'], null=True, blank=True)),
            ('kota', self.gf('smart_selects.db_fields.ChainedForeignKey')(to=orm['wisata.Kota'], null=True, blank=True)),
        ))
        db.send_create_signal('wisata', ['Wisata'])

        # Adding model 'Gallery'
        db.create_table('wisata_gallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('wisata', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wisata.Wisata'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False, max_length=5)),
        ))
        db.send_create_signal('wisata', ['Gallery'])

        # Adding model 'Comment'
        db.create_table('wisata_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('wisata', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wisata.Wisata'])),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tanggal', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('wisata', ['Comment'])

        # Adding model 'Like'
        db.create_table('wisata_like', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('wisata', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wisata.Wisata'])),
            ('like', self.gf('django.db.models.fields.BooleanField')(default=False, max_length=10)),
        ))
        db.send_create_signal('wisata', ['Like'])

        # Adding unique constraint on 'Like', fields ['user', 'wisata']
        db.create_unique('wisata_like', ['user_id', 'wisata_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Like', fields ['user', 'wisata']
        db.delete_unique('wisata_like', ['user_id', 'wisata_id'])

        # Deleting model 'Kategori'
        db.delete_table('wisata_kategori')

        # Deleting model 'Propinsi'
        db.delete_table('wisata_propinsi')

        # Deleting model 'Kota'
        db.delete_table('wisata_kota')

        # Deleting model 'Wisata'
        db.delete_table('wisata_wisata')

        # Deleting model 'Gallery'
        db.delete_table('wisata_gallery')

        # Deleting model 'Comment'
        db.delete_table('wisata_comment')

        # Deleting model 'Like'
        db.delete_table('wisata_like')


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
        'wisata.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tanggal': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'wisata': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wisata.Wisata']"})
        },
        'wisata.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '5'}),
            'wisata': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wisata.Wisata']"})
        },
        'wisata.kategori': {
            'Meta': {'object_name': 'Kategori'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kategori': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wisata.kota': {
            'Meta': {'object_name': 'Kota'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nama_kota': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'propinsi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wisata.Propinsi']"})
        },
        'wisata.like': {
            'Meta': {'unique_together': "(('user', 'wisata'),)", 'object_name': 'Like'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'wisata': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wisata.Wisata']"})
        },
        'wisata.propinsi': {
            'Meta': {'object_name': 'Propinsi'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nama_propinsi': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ordinat': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'wisata.wisata': {
            'Meta': {'object_name': 'Wisata'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'kategori': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wisata.Kategori']", 'null': 'True', 'blank': 'True'}),
            'kota': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['wisata.Kota']", 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'propinsi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wisata.Propinsi']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wisata']