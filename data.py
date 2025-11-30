import random
import string
from faker import Faker

fake=Faker()



class Urls:


    main_url = 'https://qa-scooter.praktikum-services.ru'

    
    #  COURIERS endpoints ---------------------------------

    courier_login_ep = f'{main_url}/api/v1/courier/login'
    
    courier_creation_ep = f'{main_url}/api/v1/courier'

    @classmethod
    def courier_deletion_ep (cls, id):
        return f'{cls.main_url}/api/v1/courier/{id}'

    @classmethod 
    def couriers_order_list_ep (cls, id):
        return f'{cls.main_url}/api/v1/courier/{id}/ordersCount'



    #  ORDERS endpoints --------------------------------------

    @classmethod
    def order_finish_ep (cls, id):
        return f'{cls.main_url}/api/v1/orders/finish/{id}'
    
    order_cancel_ep = f'{main_url}/api/v1/orders/cancel'

    order_creation_ep = f'{main_url}/api/v1/orders' #POST

    order_list_ep = f'{main_url}/api/v1/orders' # GET

    order_cancellation_ep = f'{main_url}/api/v1/orders/cancel'  # PUT







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

