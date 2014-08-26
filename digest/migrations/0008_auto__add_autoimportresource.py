# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AutoImportResource'
        db.create_table(u'digest_autoimportresource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('type_res', self.gf('django.db.models.fields.CharField')(default='twitter', max_length=255)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digest.Resource'], null=True, blank=True)),
            ('incl', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('excl', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('in_edit', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'digest', ['AutoImportResource'])


    def backwards(self, orm):
        # Deleting model 'AutoImportResource'
        db.delete_table(u'digest_autoimportresource')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'digest.autoimportresource': {
            'Meta': {'object_name': 'AutoImportResource'},
            'excl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'incl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digest.Resource']", 'null': 'True', 'blank': 'True'}),
            'type_res': ('django.db.models.fields.CharField', [], {'default': "'twitter'", 'max_length': '255'})
        },
        u'digest.issue': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'Issue'},
            'date_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'published_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('concurrency.fields.IntegerVersionField', [], {'name': "'version'", 'db_tablespace': "''"})
        },
        u'digest.item': {
            'Meta': {'object_name': 'Item'},
            'created_at': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_editors_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digest.Issue']", 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'related_to_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 8, 26, 0, 0)'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digest.Resource']", 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digest.Section']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'version': ('concurrency.fields.IntegerVersionField', [], {'name': "'version'", 'db_tablespace': "''"})
        },
        u'digest.resource': {
            'Meta': {'object_name': 'Resource'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('concurrency.fields.IntegerVersionField', [], {'name': "'version'", 'db_tablespace': "''"})
        },
        u'digest.section': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'Section'},
            'habr_icon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('concurrency.fields.IntegerVersionField', [], {'name': "'version'", 'db_tablespace': "''"})
        }
    }

    complete_apps = ['digest']