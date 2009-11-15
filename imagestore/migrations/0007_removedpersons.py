
from south.db import db
from django.db import models
from imagestore.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting field 'Image.author'
        db.delete_column('imagestore_image', 'author_id')
        
        # Changing field 'Image.tags'
        # (to signature: tagging.fields.TagField())
        db.alter_column('imagestore_image', 'tags', orm['imagestore.image:tags'])
        
        # Changing field 'Image.image'
        # (to signature: django.db.models.fields.files.ImageField(max_length=100))
        db.alter_column('imagestore_image', 'image', orm['imagestore.image:image'])
        
    
    
    def backwards(self, orm):
        
        # Adding field 'Image.author'
        db.add_column('imagestore_image', 'author', orm['imagestore.image:author'])
        
        # Changing field 'Image.tags'
        # (to signature: TagField(_('Tags'), blank=True))
        db.alter_column('imagestore_image', 'tags', orm['imagestore.image:tags'])
        
        # Changing field 'Image.image'
        # (to signature: ImageWithThumbnailsField(extra_thumbnails={'icon':{'size':(16,16),'options':['crop','upscale'],'extension':'jpg'},'small':{'size':(70,70),'extension':'jpg'},'preview':{'size':(120,120),'extension':'jpg'},'display':{'size':(700,900),'extension':'jpg'},}, thumbnail={'size':(100,100)}))
        db.alter_column('imagestore_image', 'image', orm['imagestore.image:image'])
        
    
    
    models = {
        'imagestore.category': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
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
