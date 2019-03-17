from django.db import models
from django.db import migrations
import django.db.models.deletion
import swapper


class Migration(migrations.Migration):

    dependencies = [
        ('imagestore_cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            'imagestorealbumptr',
            name='album',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=swapper.get_model_name('imagestore', 'Album'),
                verbose_name='Album'),
        ),
        migrations.AlterField(
            model_name='imagestorealbumcarousel',
            name='album',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=swapper.get_model_name('imagestore', 'Album'),
                verbose_name='Album'),
        ),
    ]
