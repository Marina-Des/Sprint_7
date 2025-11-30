import pytest
import allure
from reqs import OrderRequests as OrderReqs
from data import GenerateData as GenData




class TestOrders:


    #  ПРОВЕРКИ:
    #  Создание заказа
    #   Проверь, что, когда создаёшь заказ:
    #     можно указать один из цветов — BLACK или GREY; №2, №3
    #     можно указать оба цвета; №1
    #     можно совсем не указывать цвет; №4
    #     тело ответа содержит track. - в assert
    #     Чтобы протестировать создание заказа, нужно использовать параметризацию - есть

    @allure.title('Создание заказа при разных комбинациях цвета')
    @allure.description('Проверка возможности указания всех цветов, только одного и ни одного в данных заказа')
    @pytest.mark.parametrize('is_black,is_grey', [
        [True,True],
        [True,False],
        [False,True],
        [False,False]
    ])
    def test_colors_in_order (self, order_cancel_after_test, is_black, is_grey):
        order_data = GenData.data_for_order_creation()
        is_black and order_data['color'].append('BLACK')
        is_grey and order_data['color'].append('GREY')
        response = OrderReqs.order_creation_req(order_data)
        order_cancel_after_test(response.json().get('track'))
        assert response.status_code == 201 and (response.json().get('track'))




    #  ПРОВЕРКА:
    #   Список заказов
    #       Проверь, что в тело ответа возвращается список заказов.


    @allure.title('Получение списка заказов')
    @allure.description('Проверка получения списка заказов в ответ на запрос')
    def test_get_list_of_orders (self):
        response = OrderReqs.orders_list_req() # получаем весь список без фильтров
        orders = response.json()
        assert (response.status_code == 200) and (orders.get('orders')) and (type(orders.get('orders')) == list)





"""
Создание заказа
Проверь, что, когда создаёшь заказ:
    можно указать один из цветов — BLACK или GREY;
    можно указать оба цвета;
    можно совсем не указывать цвет;
    тело ответа содержит track.
    Чтобы протестировать создание заказа, нужно использовать параметризацию.

Список заказов
    Проверь, что в тело ответа возвращается список заказов.
    
"""
