from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0009_checkin'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
