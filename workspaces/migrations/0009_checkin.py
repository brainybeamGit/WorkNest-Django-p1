
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0008_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_time', models.DateTimeField(blank=True, null=True)),
                ('check_out_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Checked In', 'Checked In'), ('Checked Out', 'Checked Out')], default='Checked In', max_length=20)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='checkin', to='workspaces.booking')),
            ],
        ),
    ]
