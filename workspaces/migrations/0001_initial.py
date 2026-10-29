
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('workspace_type', models.CharField(choices=[('Hot Desk', 'Hot Desk'), ('Private Cabin', 'Private Cabin'), ('Meeting Room', 'Meeting Room')], max_length=50)),
                ('description', models.TextField()),
                ('price_per_hour', models.DecimalField(decimal_places=2, max_digits=8)),
                ('capacity', models.PositiveIntegerField(default=1)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
