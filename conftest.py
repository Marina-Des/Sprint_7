import pytest
import allure

from reqs import CourierRequests as CouReqs
from data import GenerateData as GenData



@pytest.fixture
def courier_create ():
    with allure.step('Фикстура, создает аккаунт курьера, после теста его удаляет'):
        pass
    data = GenData.data_for_courier_creation_random()
    response_creation=CouReqs.courier_creation_req(data)
    id = CouReqs.login_and_get_courier_id_by_login_password_req(data['login'], data['password']).json()['id']
    yield data
          
    CouReqs.courier_deletion_req(id)