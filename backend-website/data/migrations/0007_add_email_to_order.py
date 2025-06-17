from django.db import migrations, models

def set_default_values(apps, schema_editor):
    Order = apps.get_model('data', 'Order')
    for order in Order.objects.all():
        # Set default values for all required fields
        order.email = order.user.email if order.user else 'no-email@example.com'
        order.address = 'Default Address'
        order.city = 'Default City'
        order.state = 'Default State'
        order.pincode = '000000'
        order.phone_number = '0000000000'
        order.save()

class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='no-email@example.com'),
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(default='Default Address'),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=100, default='Default City'),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(max_length=100, default='Default State'),
        ),
        migrations.AddField(
            model_name='order',
            name='pincode',
            field=models.CharField(max_length=6, default='000000'),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=15, default='0000000000'),
        ),
        migrations.RunPython(set_default_values),
    ]