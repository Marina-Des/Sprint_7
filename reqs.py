import requests
import allure
from urls import Urls


# Здесь собраны все запросы

class CourierRequests:


    @classmethod
    @allure.step('Запрос на создание аккаунта курьера')
    def courier_creation_req (cls, data):
        response = requests.post(Urls.courier_creation_ep, data)
        return response
    

    @classmethod    
    @allure.step('Запрос на логин курьера в системе и получения id курьера по логину и паролю')
    def login_and_get_courier_id_by_login_password_req (cls, auth_data):
        response = requests.post(Urls.courier_login_ep, data=auth_data)
        return response


    @classmethod
    @allure.step('Запрос на удаление аккаунта курьера по id курьера')
    def courier_deletion_req (cls, id):
        response = requests.delete(Urls.courier_deletion_ep(id))
        return response
    


class OrderRequests:

    @classmethod
    @allure.step('Запрос на создание заказа')
    def order_creation_req (cls, order_data):
        response = requests.post(Urls.order_creation_ep, data=order_data)
        return response
    

    @classmethod
    @allure.step('Запрос на получение списка заказов')
    def orders_list_req (cls, courierId=None, nearestStation=None, limit=None, page=None):
        filter_data = {}
        if courierId:
            filter_data['courierId']=courierId
        if nearestStation:
            filter_data['nearestStation']=nearestStation
        if limit:
            filter_data['limit']=limit
        if page:
            filter_data['page']=page
        response = requests.get(Urls.order_list_ep, filter_data)
        return response


    @classmethod
    @allure.step('Запрос на отмену заказа по его track')
    def order_cancellation_by_track_req (cls, track):
        response = requests.put(Urls.order_cancellation_ep, data = {'track': track})
        return response