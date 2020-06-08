import pytest
from flask import session,jsonify 
import json

class TestAuth:

    @pytest.mark.parametrize(('login', 'password', 'email', 'status_code'), (
    ('filip','haslo','filip_email',200),
    ('', '', '', 400),
    ('filip','','filip_email',400),
    ('filip','pass','',400),
    ('','pass','filip_email',400),
    ))
    def test_sign_up_empty_fields(self, client, login, password, email, status_code):
        data = {"login": login, "password": password, "email":email}
        url = '/signup'
        response = client.post(url, json=data)
        assert response.status_code == status_code, response.get_json()

    @pytest.mark.parametrize(('login', 'password', 'email', 'email2', 'login2','status_code'), (
    ('filip','pass','email', 'email2', 'filip2',200),
    ('filip','pass','email','email', 'filip2',400),
    ('filip','pass','email','email2', 'filip',400)))
    def test_sign_up_already_exists(self, client, login, password, email, email2, login2, status_code):
        data = {"login": login, "password": password, "email":email}
        url = '/signup'
        response = client.post(url, json=data)

        data = {"login": login2, "password": password, "email":email2}
        response = client.post(url, json=data)
        assert response.status_code == status_code, response.get_json()


    @pytest.mark.parametrize(('login', 'password', 'email', 'login2', 'password2','status_code'), (
    ('filip','pass','email','filip', 'pass',200),
    ('filip','pass','email','filip', 'pass2',400),
    ('filip','pass','email','filip2', 'pass',400)))
    def test_login(self, client, login, password, email, login2, password2, status_code):
        data = {"login": login, "password": password, "email":email}
        url = '/signup'
        response = client.post(url, json=data)
        assert (response.status_code == 200) and (response.get_json() is not None), response.get_json()      
        data = {"login": login2, "password": password2}
        url = '/login'
        response = client.post(url, json=data)
        assert response.status_code == status_code, response.get_json()
