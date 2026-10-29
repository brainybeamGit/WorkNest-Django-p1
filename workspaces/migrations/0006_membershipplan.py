
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0005_workspace_amenities'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration_days', models.PositiveIntegerField(default=30)),
                ('free_hours', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
