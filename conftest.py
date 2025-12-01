import pytest
import allure

from reqs import CourierRequests as CouReqs
from reqs import OrderRequests as OrderReqs
from data import GenerateData as GenData



@pytest.fixture
def courier_create ():
    with allure.step('Фикстура, создает аккаунт курьера, после теста его удаляет'):
        pass
    data = GenData.data_for_courier_creation_random()
    response_creation=CouReqs.courier_creation_req(data)
    id = CouReqs.login_and_get_courier_id_by_login_password_req(data).json()['id']
    yield data
          
    CouReqs.courier_deletion_req(id)


@pytest.fixture
def courier_delete_after_test ():
    with allure.step('Фикстура после теста удаляет созданный в ходе теста аккаунт курьера'):
        pass
    created_courier_data ={}
    def _courier_delete_after_test (data):
        created_courier_data = data

    yield _courier_delete_after_test

    auth_data={}
    created_courier_data.get('login') and auth_data.update({'login': created_courier_data.get('login')})
    created_courier_data.get('password') and auth_data.update({'password': created_courier_data.get('password')})

    response={}
    created_courier_data.get('login') and created_courier_data.get('password') and response.update({'id': CouReqs.login_and_get_courier_id_by_login_password_req(auth_data).json().get('id')})

    CouReqs.courier_deletion_req(response.get('id'))




@pytest.fixture
def order_cancel_after_test ():
    with allure.step('Фикстура после теста отменяет созданный в ходе теста заказ'):
        pass
    created_order_id = ''
    def _order_cancel_after_test(id):
        created_order_id = id
    yield _order_cancel_after_test

    response = OrderReqs.order_cancellation_by_track_req(id)
