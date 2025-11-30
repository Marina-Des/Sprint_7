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
    @pytest.mark.parametrize('is_login,is_password,is_firstname,is_test_correct',[
        [1,1,1,True],
        [1,1,0,True],
        [1,0,1,False],
        [0,1,1,False]
        ]) # поле непустое - 1, поле пустое - 0 
    def test_courier_creation_with_different_fields_filling (self, is_login, is_password,is_firstname, is_test_correct):
        data = {}
        if is_login:
            data['login']=GenData.generate_random_string(8)
        if is_password:
            data['password']=GenData.generate_random_string(8)
        if is_firstname:
            data['firstName']=GenData.generate_random_string(8)
        response = CouReqs.courier_creation_req(data)
        try:
            assert \
            (is_test_correct and response.status_code==201 and response.text == '{"ok":true}') \
            or ((not is_test_correct) and response.status_code==400)
        finally:
            if data.get('login') and data.get('password'):
                id = CouReqs.login_and_get_courier_id_by_login_password_req(data['login'], data['password']).json()['id']
                CouReqs.courier_deletion_req(id)



    #  ПРОВЕРКИ:
    #     нельзя создать двух одинаковых курьеров;
    #     если создать пользователя с логином, который уже есть, возвращается ошибка.
    @allure.title('Создание уже существующего аккаунта курьера')
    @allure.description('Попытка создания курьера с уже существующими в базе данными.')
    def test_two_identical_couriers_creation_error (self, courier_create):
        data = courier_create
        response = CouReqs.courier_creation_req(data)
        assert response.status_code == 409 

        
    #  ПРОВЕРКИ:
    #    курьер может авторизоваться; - №1
    #    для авторизации нужно передать все обязательные поля; - №1
    #    если какого-то поля нет, запрос возвращает ошибку; - №2, №3, №4
    #    успешный запрос возвращает id. - в assert


    @allure.title('Авторизация при присутствующих/отсутствующих полях логина и пароля')
    @allure.description('Проверка успешной авторизации при наличии обоих полей с верными данными и получения ошибки при отсутствии одного из полей или обоих.')
    @pytest.mark.parametrize('is_login,is_password,target_status_code',[
        [1,1,200],
        [1,0,400],
        [0,1,400],
        [0,0,400]
    ])
    # КОММЕНТАРИЙ:
    # В этом тесте при отправке на сервер данных без поля password сервер долго думает и присылает 504 service unavailable. При этом без поля login - все по доке, ошибка 400 "недостаточно данных". Пробовала в разные дни. 2 теста здесь падают из-за assertion error.  
    # Я проверила и в отдельном файле именно сам запрос, и вручную в Postman'е. 
    def test_courier_authorization (self, courier_create, is_login, is_password, target_status_code):
        auth_data = courier_create
        if not is_login:
            auth_data['login']=None
        if not is_password:
            auth_data['password']=None
        response = CouReqs.login_and_get_courier_id_by_login_password_req(auth_data.get('login'), auth_data.get('password') )
        assert response.status_code == target_status_code
       


    #  ПРОВЕРКИ:
    #   система вернёт ошибку, если неправильно указать логин или пароль;
    #   если авторизоваться под несуществующим пользователем, запрос возвращает ошибку;
    
    @allure.title('Авторизация при неверных значениях логина и пароля')
    @allure.description('Проверка получения ошибки при неправильных комбинациях логина и пароля.')
    @pytest.mark.parametrize('with_login, with_password, target_status_code', [
        ['','',200],
        ['abc','',404],
        ['','123',404],
        ['bca','321',404]
    ])
    def test_wrong_login_and_password (self, courier_create, with_login, with_password, target_status_code):

        response = CouReqs.login_and_get_courier_id_by_login_password_req(courier_create.get('login')+with_login, courier_create.get('password')+with_password)

        assert response.status_code == target_status_code and ( (not response.status_code == 200) or (response.json().get('id')))



# ДОПОЛНИТЕЛЬНЫЕ
# Удалить курьера
# Проверь:
#     неуспешный запрос возвращает соответствующую ошибку;
#     успешный запрос возвращает{"ok":true};
#     если отправить запрос без id, вернётся ошибка;
#     если отправить запрос с несуществующим id, вернётся ошибка.

    #  КОММЕНТАРИЙ
    #  При статусах 400 и 404 фактическое тело ответа отличается от того, что в документации. По факту в теле есть еще поле 'code'. На мой взгляl, это ошибка, надо уточнять с разработчиками бэкэнда. Поэтому 2 теста падают.

    @allure.title('Удаление курьера')
    @allure.description('Проверка полученных статусов-кодов и сообщений при запросе на удаление курьера')
    @pytest.mark.parametrize('is_id, with_id, target_status_code, target_body', [
        [True, 0, 200, {"ok": True}],
        [True, 10102345, 404, {"message": "Курьера с таким id нет"}],
        [False, 0, 400, {"message": "Недостаточно данных для удаления курьера"}]
    ])
    def test_courier_deletion (self, courier_create, is_id, with_id, target_status_code, target_body):
        if is_id:
            id = CouReqs.login_and_get_courier_id_by_login_password_req(courier_create.get('login'), courier_create.get('password')).json().get('id') + with_id
        else: 
            id=''

        response = CouReqs.courier_deletion_req(id)
        
        assert (response.status_code == target_status_code) and (response.json() == target_body) 






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