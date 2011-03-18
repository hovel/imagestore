# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('imagestore_category')

        # Adding field 'Album.user'
        db.add_column('imagestore_album', 'user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='albums', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Album.is_public'
        db.add_column('imagestore_album', 'is_public', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Album.head'
        db.add_column('imagestore_album', 'head', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='head_of', null=True, to=orm['imagestore.Image']), keep_default=False)

        # Deleting field 'Image.is_public'
        db.delete_column('imagestore_image', 'is_public')

        # Deleting field 'Image.category'
        db.delete_column('imagestore_image', 'category_id')

        # Adding field 'Image.album'
        db.add_column('imagestore_image', 'album', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='images', null=True, to=orm['imagestore.Album']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('imagestore_category', (
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['imagestore.Category'], blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('imagestore', ['Category'])

        # Deleting field 'Album.user'
        db.delete_column('imagestore_album', 'user_id')

        # Deleting field 'Album.is_public'
        db.delete_column('imagestore_album', 'is_public')

        # Deleting field 'Album.head'
        db.delete_column('imagestore_album', 'head_id')

        # Adding field 'Image.is_public'
        db.add_column('imagestore_image', 'is_public', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'Image.category'
        db.add_column('imagestore_image', 'category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', null=True, to=orm['imagestore.Category'], blank=True), keep_default=False)

        # Deleting field 'Image.album'
        db.delete_column('imagestore_image', 'album_id')


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
        'imagestore.album': {
            'Meta': {'ordering': "('created', 'name')", 'object_name': 'Album'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'head': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'head_of'", 'null': 'True', 'to': "orm['imagestore.Image']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'albums'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'imagestore.image': {
            'Meta': {'ordering': "('order', 'id')", 'object_name': 'Image'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'to': "orm['imagestore.Album']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['imagestore']
