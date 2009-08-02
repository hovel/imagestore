
from south.db import db
from django.db import models
from imagestore.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('imagestore_category', (
            ('id', orm['imagestore.Category:id']),
            ('slug', orm['imagestore.Category:slug']),
            ('title', orm['imagestore.Category:title']),
            ('order', orm['imagestore.Category:order']),
        ))
        db.send_create_signal('imagestore', ['Category'])
        
        # Adding model 'Image'
        db.create_table('imagestore_image', (
            ('id', orm['imagestore.Image:id']),
            ('slug', orm['imagestore.Image:slug']),
            ('title', orm['imagestore.Image:title']),
            ('description', orm['imagestore.Image:description']),
            ('tags', orm['imagestore.Image:tags']),
            ('category', orm['imagestore.Image:category']),
            ('author', orm['imagestore.Image:author']),
            ('order', orm['imagestore.Image:order']),
            ('image', orm['imagestore.Image:image']),
        ))
        db.send_create_signal('imagestore', ['Image'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('imagestore_category')
        
        # Deleting model 'Image'
        db.delete_table('imagestore_image')
        
    
    
    models = {
        'imagestore.category': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'imagestore.image': {
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Person']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['imagestore.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('ImageWithThumbnailsField', [], {'extra_thumbnails': "{'icon':{'size':(16,16),'options':['crop','upscale'],'extension':'jpg'},'small':{'size':(70,70),'extension':'jpg'},'preview':{'size':(120,120),'extension':'jpg'},'display':{'size':(700,900),'extension':'jpg'},}", 'thumbnail': "{'size':(100,100)}"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tags': ('TagField', ["_('Tags')"], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'persons.person': {
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'e_mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_premium': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'second_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tags': ('TagField', ["_('Tags')"], {'blank': 'True'})
        }
    }
    
    complete_apps = ['imagestore']
