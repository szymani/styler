import pytest
from flask import session,jsonify 
import json
from application.models import single_post_model, user_model
from application import db, ma

class TestUser:
    @pytest.mark.parametrize(('login', 'password', 'email', 'status_code'), (
    ('filip','haslo','filip_email',200),
    ))
    def test_get_user_self(self, client, app, login, password, email, status_code):
        data = {"login": login, "password": password, "email":email}
        url = '/signup'
        response = client.post(url, json=data)
        assert (response.status_code == 200) and (response.get_json() is not None), response.get_json()
        headers = {"Authorization": "Bearer " + response.get_json()["Auth_token"]}
        url = '/user'
        response = client.get(url, headers=headers, follow_redirects=True)
        assert response.status_code == status_code, response.get_json()


    @pytest.mark.parametrize(('login', 'password', 'email', 'login2', 'password2', 'email2', 'status_code'), (
    ('filip','pass','email','filip2', 'pass2', 'email2',200),))
    def test_update_user_self(self, client, app, login, password, email, login2, password2, email2, status_code):
        data = {"login": login, "password": password, "email":email}
        url = '/signup'
        response = client.post(url, json=data)
        assert (response.status_code == 200) and (response.get_json() is not None), response.get_json()
        headers = {"Authorization": "Bearer " + response.get_json()["Auth_token"]}
        data = {"login": login2, "password": password2, "email":email2}
        url = '/user'
        response = client.put(url, json=data,headers=headers, follow_redirects=True)
        assert (response.status_code == 200) and (response.get_json() is not None), response.get_json()
        assert response.get_json()["login"] == data["login"]


    @pytest.mark.parametrize(('login', 'password', 'email','status_code'), (
    ('filip','pass','email',200),))
    def test_delete_user_self(self, client, app, login, password, email, status_code):
        data = {"login": login, "password": password, "email":email}
        url = '/signup'
        response = client.post(url, json=data)
        assert (response.status_code == 200) and (response.get_json() is not None), response.get_json()    
        headers = {"Authorization": "Bearer " + response.get_json()["Auth_token"]}
        url = '/user'
        response = client.delete(url, headers=headers, follow_redirects=True)
        assert response.status_code == status_code, response.get_json()


    @pytest.mark.parametrize(( 'login', 'password','user_type','status_code'), (
    ( 'login', 'password','1',200),('login', 'password','0',401),))
    def test_get_user_by_id(self, client, login, password, user_type, status_code):
        first_user = user_model.User(login= login,password=password, email="admin_email", user_type=user_type)
        second_user = user_model.User(login="someLogin",password="somePassword", email="someEmail", user_type=0)        
        db.session.add(first_user, second_user)
        db.session.commit()

        data = {"login": login, "password": password}
        url = '/login'
        response = client.post(url, json=data)
        assert (response.status_code == 200) and (response.get_json() is not None), response.get_json()
        headers = {"Authorization": "Bearer " + response.get_json()["Auth_token"]}
        url = '/user/1'
        response = client.get(url, headers=headers)
        assert response.status_code == status_code, response.get_json()


    @pytest.mark.parametrize(('login', 'password', 'email', 'login2', 'password2', 'email2','user_type', 'status_code'), (
    ('filip','pass','email','filip2', 'pass2', 'email2',1 , 200),))
    def test_update_user_by_id(self, client, app, login, password, email, login2, password2, email2, user_type, status_code):
        first_user = user_model.User(login= login,password=password, email=email, user_type=user_type)
        second_user = user_model.User(login="someLogin",password="somePassword", email="someEmail", user_type=0)        
        db.session.add(first_user, second_user)
        db.session.commit()
       
        data = {"login": login, "password": password}
        url = '/login'
        response = client.post(url, json=data)
        assert (response.status_code == 200) and (response.get_json() is not None), response.get_json()
        headers = {"Authorization": "Bearer " + response.get_json()["Auth_token"]}
        data = {"login": login2, "password": password2, "email":email2}
        url = '/user/1'
        response = client.put(url, json=data,headers=headers)
        assert (response.status_code == 200) and (response.get_json() is not None), response.get_json()


    @pytest.mark.parametrize(( 'login', 'password','user_type','status_code'), (
    ( 'login', 'password','1',200),('login', 'password','0',401),))
    def test_delete_user_by_id(self, client, app, login, password,user_type, status_code):
        first_user = user_model.User(login= login,password=password, email="admin_email", user_type=user_type)
        second_user = user_model.User(login="someLogin",password="somePassword", email="someEmail", user_type=0)        
        db.session.add(first_user, second_user)
        db.session.commit()

        data = {"login": login, "password": password}
        url = '/login'
        response = client.post(url, json=data)
        assert (response.status_code == 200) and (response.get_json() is not None), response.get_json()
        headers = {"Authorization": "Bearer " + response.get_json()["Auth_token"]}
        url = '/user/1'
        response = client.delete(url, headers=headers)
        assert response.status_code == status_code, response.get_json()
