import pytest
import allure
from reqs import CourierRequests as CouReqs
from data import GenerateData as GenData



class TestCourier:


    #  ПРОВЕРКИ:   
    #     1. курьера можно создать; - №1
    #     2. чтобы создать курьера, нужно передать в ручку все обязательные поля; - все поля, все без одного каждого - №1,2,3,4
    #     3. запрос возвращает правильный код ответа; - в assert 201 и 400
    #     4. успешный запрос возвращает {"ok":true}; - в assert в 201
    #     5. если одного из полей нет, запрос возвращает ошибку; - №2,3,4

    @allure.title('Создание аккаунта курьера при разном заполнении полей логин-пароль-имя')
    @allure.description('Тестируется ответ сервера на попытку создания аккаунта при наличии всех полей и при наличии двух из трех полей (3 варианта)')
    @pytest.mark.parametrize('is_login,is_password,is_firstname,target_status_code, target_body',[
        [True,True,True,201,("ok",True)],
        [True,True,False,201,("ok",True)],
        [True,False,True,400,("message","Недостаточно данных для создания учетной записи")],
        [False,True,True,400,("message","Недостаточно данных для создания учетной записи")]
        ]) 
    def test_courier_creation_with_different_fields_filling (self, courier_delete_after_test,  is_login, is_password,is_firstname, target_status_code, target_body):
        data = {}
        is_login and data.update({'login': GenData.generate_random_string(8)})
        is_password and data.update({'password': GenData.generate_random_string(8)})
        is_firstname and data.update({'firstName': GenData.generate_random_string(8)})
        response = CouReqs.courier_creation_req(data)
        courier_delete_after_test(data)
        assert \
            (response.status_code == target_status_code) and \
            (target_body in response.json().items()) 




    #  ПРОВЕРКИ:
    #     нельзя создать двух одинаковых курьеров;
    #     если создать пользователя с логином, который уже есть, возвращается ошибка.
    @allure.title('Создание уже существующего аккаунта курьера')
    @allure.description('Попытка создания курьера с уже существующими в базе данными.')
    def test_two_identical_couriers_creation_error (self, courier_create):
        data = courier_create
        response = CouReqs.courier_creation_req(data)
        assert \
            (response.status_code == 409) and \
            (("message", "Этот логин уже используется") in response.json().items())


        
    #  ПРОВЕРКИ:
    #    курьер может авторизоваться; - №1
    #    для авторизации нужно передать все обязательные поля; - №1
    #    если какого-то поля нет, запрос возвращает ошибку; - №2, №3, №4
    #    успешный запрос возвращает id. - в assert




    @allure.title('Авторизация при присутствующих и существующих логине и пароле')
    @allure.description('Проверка успешной авторизации при наличии обоих полей с верными данными.')
    def test_courier_authorization_login_password (self, courier_create):
        response = CouReqs.login_and_get_courier_id_by_login_password_req({'login': courier_create.get('login'), 'password': courier_create.get('password')})
        assert \
            (response.status_code == 200) and \
            (response.json().get('id'))
        



    @allure.title('Авторизация при отсутствующих полях логина и пароля')
    @allure.description('Проверка получения ошибки при отсутствии одного из полей логин, пароль или обоих.')
    @pytest.mark.parametrize('is_login,is_password,target_status_code,body_key,body_value',[
        [True,None,400,'message','Недостаточно данных для входа'],
        [None,True,400,'message','Недостаточно данных для входа'],
        [None,None,400,'message','Недостаточно данных для входа']
    ]) 
    def test_courier_authorization (self, courier_create, is_login, is_password, target_status_code, body_key, body_value):
        auth_data = {}
        is_login and auth_data.update({'login': courier_create.get('login')})
        is_password and auth_data.update({'password': courier_create.get('password')})
        response = CouReqs.login_and_get_courier_id_by_login_password_req(auth_data)
        assert \
            (response.status_code == target_status_code) and \
            ((body_key, body_value) in response.json().items())
       


    #  ПРОВЕРКИ:
    #   система вернёт ошибку, если неправильно указать логин или пароль;
    #   если авторизоваться под несуществующим пользователем, запрос возвращает ошибку;
    
    @allure.title('Авторизация при неверных значениях логина и пароля')
    @allure.description('Проверка получения ошибки при неправильных комбинациях логина и пароля.')
    @pytest.mark.parametrize('with_login, with_password, target_status_code,target_body', [
        ['abc','',404,('message','Учетная запись не найдена')],
        ['','123',404,('message','Учетная запись не найдена')],
        ['bca','321',404,('message','Учетная запись не найдена')]
    ])
    def test_wrong_login_and_password (self, courier_create, with_login, with_password, target_status_code, target_body):
        auth_data = {
            'login': courier_create.get('login')+with_login,
            'password': courier_create.get('password')+with_password
        }
        response = CouReqs.login_and_get_courier_id_by_login_password_req(auth_data)

        assert \
            (response.status_code == target_status_code) and \
            (target_body in response.json().items())


# ДОПОЛНИТЕЛЬНЫЕ
# Удалить курьера
# Проверь:
#     неуспешный запрос возвращает соответствующую ошибку;
#     успешный запрос возвращает{"ok":true};
#     если отправить запрос без id, вернётся ошибка;
#     если отправить запрос с несуществующим id, вернётся ошибка.


    @allure.title('Удаление курьера')
    @allure.description('Проверка полученных статусов-кодов и сообщений при запросе на удаление курьера')
    @pytest.mark.parametrize('is_id, with_id, target_status_code, target_body', [
        [True, 0, 200, ("ok", True)],
        [True, 10102345, 404, ("message", "Курьера с таким id нет")], # в документации без точки в конце, по факту от сервера - с точкой. Поэтому падает. 
        [False, 0, 400, ("message", "Недостаточно данных для удаления курьера")]
    ])
    def test_courier_deletion (self, courier_create, is_id, with_id, target_status_code, target_body):
        auth_data = {
            'login': courier_create.get('login'),
            'password': courier_create.get('password')
        }
        id = {True: CouReqs.login_and_get_courier_id_by_login_password_req(auth_data).json().get('id') + with_id,
              False: ''}
        
        response = CouReqs.courier_deletion_req(id.get(is_id))
        
        assert (response.status_code == target_status_code) and (target_body in response.json().items()) 



"""
Создание курьера
Проверь:
    курьера можно создать;
    нельзя создать двух одинаковых курьеров;
    чтобы создать курьера, нужно передать в ручку все обязательные поля;
    запрос возвращает правильный код ответа;
    успешный запрос возвращает {"ok":true};
    если одного из полей нет, запрос возвращает ошибку;
    если создать пользователя с логином, который уже есть, возвращается ошибка.
    
"""


"""
Логин курьера
Проверь:
    курьер может авторизоваться;
    для авторизации нужно передать все обязательные поля;
    система вернёт ошибку, если неправильно указать логин или пароль;
    если какого-то поля нет, запрос возвращает ошибку;
    если авторизоваться под несуществующим пользователем, запрос возвращает ошибку;
    успешный запрос возвращает id.
    
"""