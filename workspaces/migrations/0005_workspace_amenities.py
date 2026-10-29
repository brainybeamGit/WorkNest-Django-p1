
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0004_amenity'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='amenities',
            field=models.ManyToManyField(blank=True, related_name='workspaces', to='workspaces.amenity'),
        ),
    ]
