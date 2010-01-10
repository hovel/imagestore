
from south.db import db
from django.db import models
from imagestore.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Category.parent_category'
        db.add_column('imagestore_category', 'parent_category', orm['imagestore.category:parent_category'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Category.parent_category'
        db.delete_column('imagestore_category', 'parent_category_id')
        
    
    
    models = {
        'imagestore.category': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['imagestore.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'imagestore.image': {
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['imagestore.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['imagestore']
