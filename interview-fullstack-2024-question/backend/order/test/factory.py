import factory
import faker

from order.models import Address, Order, OrderItem


fake = faker.Factory.create()


class AddressFactory(factory.django.DjangoModelFactory):
    address_line_1 = factory.Faker('street_address')
    address_line_2 = factory.Faker('secondary_address')
    city = factory.Faker('city')
    state = factory.Faker('state_abbr')
    postal_code = factory.Faker('zipcode')
    phone_number = factory.Faker('phone_number')

    class Meta:
        model = Address


class OrderItemFactory(factory.django.DjangoModelFactory):
    sku = factory.Faker('pystr', min_chars=3, max_chars=10)
    quantity = factory.Faker('pyint', min_value=1, max_value=10)
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)

    class Meta:
        model = OrderItem


class OrderFactory(factory.django.DjangoModelFactory):
    address = factory.SubFactory(AddressFactory)
    order_number = factory.Faker('pystr', prefix='ORD#', max_chars=10)
    ordered_at = factory.Faker('date_time_between', start_date='-1y', end_date='now')

    @factory.post_generation
    def order_items(self, create, extracted, **kwargs):
        if not create:
            return

        size = fake.random.randint(1, 5) if extracted is None else extracted
        OrderItemFactory.create_batch(size, order=self, **kwargs)

    class Meta:
        model = Order
