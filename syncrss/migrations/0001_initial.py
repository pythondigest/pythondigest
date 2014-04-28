# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResourceRSS'
        db.create_table(u'syncrss_resourcerss', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sync_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=2)),
            ('version', self.gf('concurrency.fields.IntegerVersionField')(name='version', db_tablespace='')),
        ))
        db.send_create_signal(u'syncrss', ['ResourceRSS'])

        # Adding model 'RawItem'
        db.create_table(u'syncrss_rawitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['digest.Section'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('resource_rss', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['syncrss.ResourceRSS'], null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('related_to_date', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=10)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('version', self.gf('concurrency.fields.IntegerVersionField')(name='version', db_tablespace='')),
        ))
        db.send_create_signal(u'syncrss', ['RawItem'])


    def backwards(self, orm):
        # Deleting model 'ResourceRSS'
        db.delete_table(u'syncrss_resourcerss')

        # Deleting model 'RawItem'
        db.delete_table(u'syncrss_rawitem')


    models = {
        u'digest.section': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'Section'},
            'habr_icon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('concurrency.fields.IntegerVersionField', [], {'name': "'version'", 'db_tablespace': "''"})
        },
        u'syncrss.rawitem': {
            'Meta': {'object_name': 'RawItem'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'related_to_date': ('django.db.models.fields.DateField', [], {}),
            'resource_rss': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['syncrss.ResourceRSS']", 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['digest.Section']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '10'}),
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