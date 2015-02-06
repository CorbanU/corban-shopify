# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, serialize=False, editable=False, primary_key=True)),
                ('topic', models.CharField(max_length=32, choices=[('orders/create', 'Order creation'), ('orders/delete', 'Order deletion'), ('orders/updated', 'Order update'), ('orders/paid', 'Order payment'), ('orders/cancelled', 'Order cancellation'), ('orders/fulfilled', 'Order fulfillment'), ('carts/create', 'Cart creation'), ('carts/update', 'Cart update'), ('checkouts/create', 'Checkout creation'), ('checkouts/update', 'Checkout update'), ('checkouts/delete', 'Checkout deletion'), ('refunds/create', 'Refund create'), ('products/create', 'Product creation'), ('products/update', 'Product update'), ('products/delete', 'Product deletion'), ('collections/create', 'Collection creation'), ('collections/update', 'Collection update'), ('collections/delete', 'Collection deletion'), ('customer_groups/create', 'Customer group creation'), ('customer_groups/update', 'Customer group update'), ('customer_groups/delete', 'Customer group deletion'), ('customers/create', 'Customer creation'), ('customers/enable', 'Customer enable'), ('customers/disable', 'Customer disable'), ('customers/update', 'Customer update'), ('customers/delete', 'Customer deletion'), ('fulfillments/create', 'Fulfillment creation'), ('fulfillments/update', 'Fulfillment update'), ('shop/update', 'Shop update')])),
                ('webhook_id', models.IntegerField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
