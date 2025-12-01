

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




