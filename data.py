import random
import string
from faker import Faker

fake=Faker()




class GenerateData:

    @classmethod
    def generate_random_string(cls, length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @classmethod
    def data_for_courier_creation_random (cls):
        return {
            'login': cls.generate_random_string(8),
            'password': cls.generate_random_string(8),
            'firstName': fake.first_name()
        }
    
    @classmethod
    def data_for_order_creation (cls):
        return {
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'address': fake.street_address(),
            'metroStation': cls.generate_random_string(8),
            'phone': '+7 '+ fake.basic_phone_number(),
            'rentTime': fake.random_int(min=1, max=10),
            'deliveryDate': fake.date_between(start_date='+1d', end_date='+10d').strftime("%Y-%m-%d"),
            'comment': cls.generate_random_string(50),
            'color': []
        }

