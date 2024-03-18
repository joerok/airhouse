import factory
import faker

from shipment.models import Shipment, ShipmentItem

fake = faker.Factory.create()


class ShipmentFactory(factory.django.DjangoModelFactory):
    tracking_number = factory.Faker('pystr', min_chars=10, max_chars=20)
    method = factory.Faker('word')
    shipped_at = factory.Faker('date_time_between', start_date='-1y', end_date='now')

    @factory.post_generation
    def shipment_items(self, create, extracted, **kwargs):
        if not create:
            return

        for item in self.order.order_items.all():
            ShipmentItem.objects.create(shipment=self, order_item=item, quantity=item.quantity)

    class Meta:
        model = Shipment
