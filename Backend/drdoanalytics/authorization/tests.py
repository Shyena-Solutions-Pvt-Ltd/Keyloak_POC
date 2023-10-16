from django.test import TestCase
from .models import *
from .util import *
from django.conf import settings
from django.http import JsonResponse
from keycloak import KeycloakOpenID
from rest_framework.test import APIClient
from keycloak import KeycloakError, KeycloakDeleteError
import json

class KeycloakTest(TestCase):

    def __init__(self, methodName: str = "runTest") -> None:

        self.config = settings.KEYCLOAK_CONFIG
        try:
            self.server_url = self.config['KEYCLOAK_SERVER_URL']
            self.client_id = self.config['KEYCLOAK_CLIENT_ID']
            self.realm = self.config['KEYCLOAK_REALM']
            self.client_secret_key = self.config.get('KEYCLOAK_CLIENT_SECRET_KEY', None)
            self.test_user = self.config.get('KEYCLOAK_TEST_ADMIN_USER', None)
            self.test_user_password = self.config.get('KEYCLOAK_TEST_ADMIN_PASSWORD', None)
        except KeyError as e:
            raise Exception("KEYCLOAK_SERVER_URL, KEYCLOAK_CLIENT_ID or KEYCLOAK_REALM not found.")
        
        super().__init__(methodName)
        # Create Keycloak instance
        self.keycloak = KeycloakOpenID(server_url=self.server_url,
                                        client_id=self.client_id,
                                        realm_name=self.realm,
                                        client_secret_key=self.client_secret_key)

    def create_testuser(self):

        token = self.keycloak.token(self.test_user, self.test_user_password)
        token = token['access_token']
        header = {'HTTP_AUTHORIZATION': 'Bearer '+token}
        data = json.dumps({
                'email' : 'test@gmail.com',
                'username' : 'test01',
                'firstname' : 'first',
                'lastname' : 'last',
                'password' : 'test'
        })

        client = APIClient()
        response = client.post('/auth/create-user/', content_type='application/json', data=data, **header)
        response_body = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_body['status'],'user created')
    
    def delete_testuser(self):
        try:
            keycloak_admin = getKeycloakAdmin()
            user_id_keycloak = keycloak_admin.get_user_id("test01")
            response = keycloak_admin.delete_user(user_id = user_id_keycloak)
        except  KeycloakDeleteError as e:
            raise Exception("Unable to delete test user, please delete manually.")
        
    def test_connection(self):        
        client_public_key = "-----BEGIN PUBLIC KEY-----\n" + self.keycloak.public_key() + "\n-----END PUBLIC KEY-----"
        self.assertTrue(client_public_key)

    def test_created_user_login_logout(self):
        
        self.create_testuser()

        client = APIClient()

        # Test Login
        data = json.dumps({
            "username":"test01",
            "password":"test"
        })
        response = client.post('/auth/login/', content_type='application/json', data=data)
        response_body = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response_body['token'])

        # Test Logout
        data = json.dumps({
            "refresh_token":response_body['refresh_token']
        })
        header = {'HTTP_AUTHORIZATION': 'Bearer '+ response_body['token']}
        response = client.post('/auth/logout/', content_type='application/json', data=data,**header)
        response_body = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_body['detail'], "User logged out successfully.") 

        self.delete_testuser()

    def test_get_users(self):

        self.create_testuser()
        
        token = self.keycloak.token(self.test_user, self.test_user_password)
        token = token['access_token']
        client = APIClient()

        # Test Login
        header = {'HTTP_AUTHORIZATION': 'Bearer '+ token}
        response = client.get('/auth/get-users/', content_type='application/json',**header)
        response_body = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response_body['users'])

        for user in response_body['users']:
            if user['username'] == 'test01':
                return True
            
        self.delete_testuser()

        raise Exception("Unable to fetch created test user.")
    
    


