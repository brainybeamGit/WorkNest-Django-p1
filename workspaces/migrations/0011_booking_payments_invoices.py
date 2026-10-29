
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0010_payment_razorpay_order_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_type',
            field=models.CharField(choices=[('Hourly', 'Hourly'), ('Daily', 'Daily')], default='Hourly', max_length=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], default='Unpaid', max_length=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='plan_hours_used',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='payment',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='workspaces.booking'),
        ),
        migrations.AddField(
            model_name='workspace',
            name='daily_rate',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Full-day (9 AM - 6 PM) rate. Leave 0 to use 8x the hourly rate.', max_digits=8),
        ),
        migrations.AlterField(
            model_name='payment',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='workspaces.membershipplan'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=30, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='workspaces.booking')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to=settings.AUTH_USER_MODEL)),
                ('subscription', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='workspaces.subscription')),
            ],
        ),
    ]
