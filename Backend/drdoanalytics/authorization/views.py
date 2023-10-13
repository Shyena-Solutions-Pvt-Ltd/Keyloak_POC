import json
import logging
from django.http import HttpResponse,JsonResponse
from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
from keycloak import KeycloakError, KeycloakPostError
from django.conf import settings
from rest_framework import status
from .util import getKeycloak, getKeycloakAdmin

logger = logging.getLogger(__name__)

def secured_hello(request):
    logger.debug(request.user['roles'])
    return HttpResponse("Secured Hello")

def unsecured_hello(request):
    return HttpResponse("Unsecured Hello")

def login(request):
    # Configure client

    try:
        body = json.loads(request.body.decode("utf-8"))
        username = body['username']
        password = body['password']
    except Exception as e:
        return JsonResponse({"detail": "Credentials not provided."},status=status.HTTP_400_BAD_REQUEST)

    try:
        keycloak_openid = getKeycloak()
        try:
            token = keycloak_openid.token(username, password)
        except  Exception as e:
            logger.error(e)
            return JsonResponse({"detail": "Invalid user credentials."},status=status.HTTP_401_UNAUTHORIZED)
        
        resp = {
            "token" : token['access_token'], 
            "expires_in" : token['expires_in'],
            "refresh_token" : token['refresh_token'],
            "refresh_expires_in" : token['refresh_expires_in']
            }

    except Exception as e:
        logger.error(e)
        return JsonResponse({"detail": "Error Validating user credentials."},status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return JsonResponse(resp,status=status.HTTP_200_OK)

def refresh_token(request):
    try:
        try:
            body = json.loads(request.body.decode("utf-8"))
            
            refresh_token = body['refresh_token']
        except Exception as e:
            logger.error(e)
            return JsonResponse({"detail": "Pass Refresh token provided during login."},status=status.HTTP_400_BAD_REQUEST)

        keycloak_openid = getKeycloak()
        token = keycloak_openid.refresh_token(refresh_token)

        resp = {
            "token" : token['access_token'], 
            "expires_in" : token['expires_in'],
            "refresh_token" : token['refresh_token'],
            "refresh_expires_in" : token['refresh_expires_in']
            }

    except Exception as e:
        logger.error(e)
        return JsonResponse({"detail": "Error Refreshing the token. Session might have expired, login again."},status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return JsonResponse(resp,status=status.HTTP_200_OK)

def logout(request):
    try:
        try:
            body = json.loads(request.body.decode("utf-8"))
            
            refresh_token = body['refresh_token']
        except Exception as e:
            logger.error(e)
            return JsonResponse({"detail": "Pass Refresh token to logout user."},status=status.HTTP_400_BAD_REQUEST)

        keycloak_openid = getKeycloak()
        keycloak_openid.logout(refresh_token)

    except Exception as e:
        logger.error(e)
        return JsonResponse({"detail": "Error Logging out user."},status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return JsonResponse({"detail":"User logged out successfully."},status=status.HTTP_200_OK)
            
def create_user(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
        email = body["email"]
        username = body["username"]
        password = body["password"]
        firstname = body["firstname"]
        lastname = body["lastname"]
    except Exception as e:
        return JsonResponse({"detail": "Provide required Information."},status=status.HTTP_400_BAD_REQUEST)

    try:
        keycloak_admin = getKeycloakAdmin()
        try:
            new_user = keycloak_admin.create_user({
                    "email": email,
                    "username": username,
                    "enabled": True,
                    "firstName": firstname,
                    "lastName": lastname,
                    "credentials": [{"value": password,"type": "password",}]
                }
                ,exist_ok=False
            )
        except  KeycloakPostError as e:
            return JsonResponse({"detail": json.loads(e.error_message.decode("utf-8"))['errorMessage']}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(e)
        return JsonResponse({"detail": "Error occurred when creating user."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


    return JsonResponse({"status":"user created"},status=status.HTTP_200_OK)

def change_password(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
        new_password = body["new_password"]
    except Exception as e:
        return JsonResponse({"detail": "Provide a new password"},status=status.HTTP_400_BAD_REQUEST)

    try:
        keycloak_admin = getKeycloakAdmin()
        try:
            user_id_keycloak = keycloak_admin.get_user_id(request.user['username'])
            changed_password = keycloak_admin.set_user_password(user_id=user_id_keycloak, password=new_password, temporary=False)
        except  KeycloakPostError as e:
            return JsonResponse({"detail": json.loads(e.error_message.decode("utf-8"))['errorMessage']}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(e)
        return JsonResponse({"detail": "Error occurred when creating user."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return JsonResponse({"status":"password changed successfully"},status=status.HTTP_200_OK)

def get_users(request):
    
    try:
        keycloak_admin = getKeycloakAdmin()
        try:
            users = keycloak_admin.get_users({})
        except  KeycloakPostError as e:
            return JsonResponse({"detail": json.loads(e.error_message.decode("utf-8"))['errorMessage']}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(e)
        return JsonResponse({"detail": "Error occurred when creating user."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return JsonResponse({"users":users},status=status.HTTP_200_OK)