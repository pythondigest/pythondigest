# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ResourceRSS.sync_date'
        db.alter_column(u'syncrss_resourcerss', 'sync_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'ResourceRSS.sync_date'
        db.alter_column(u'syncrss_resourcerss', 'sync_date', self.gf('django.db.models.fields.DateField')(null=True))

    models = {
        u'syncrss.rawitem': {
            'Meta': {'object_name': 'RawItem'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'related_to_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('concurrency.fields.IntegerVersionField', [], {'name': "'version'", 'db_tablespace': "''"})
        },
        u'syncrss.resourcerss': {
            'Meta': {'object_name': 'ResourceRSS'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sync_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('concurrency.fields.IntegerVersionField', [], {'name': "'version'", 'db_tablespace': "''"})
        }
    }

    complete_apps = ['syncrss']