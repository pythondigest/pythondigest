# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RawItem.resource_rss'
        db.add_column(u'syncrss_rawitem', 'resource_rss',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syncrss.ResourceRSS'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'RawItem.language'
        db.add_column(u'syncrss_rawitem', 'language',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2013, 11, 20, 0, 0), max_length=2),
                      keep_default=False)

        # Adding field 'ResourceRSS.language'
        db.add_column(u'syncrss_resourcerss', 'language',
                      self.gf('django.db.models.fields.CharField')(default='en', max_length=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RawItem.resource_rss'
        db.delete_column(u'syncrss_rawitem', 'resource_rss_id')

        # Deleting field 'RawItem.language'
        db.delete_column(u'syncrss_rawitem', 'language')

        # Deleting field 'ResourceRSS.language'
        db.delete_column(u'syncrss_resourcerss', 'language')


    models = {
        u'syncrss.rawitem': {
            'Meta': {'object_name': 'RawItem'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'related_to_date': ('django.db.models.fields.DateField', [], {}),
            'resource_rss': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syncrss.ResourceRSS']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('concurrency.fields.IntegerVersionField', [], {'name': "'version'", 'db_tablespace': "''"})
        },
        u'syncrss.resourcerss': {
            'Meta': {'object_name': 'ResourceRSS'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sync_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('concurrency.fields.IntegerVersionField', [], {'name': "'version'", 'db_tablespace': "''"})
        }
    }

    complete_apps = ['syncrss']