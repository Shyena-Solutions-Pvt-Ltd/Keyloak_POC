from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from keycloak import KeycloakOpenID


   
def get_auth(request):
    
    # Configure client
    keycloak_openid = KeycloakOpenID(server_url="http://localhost:8088/auth/",
                                    client_id="web_app",
                                    realm_name="drdo_realm",
                                    client_secret_key="cPlYucFs8b3wxfWggmfQkg6yUsxLBi4P")
    
    token = {
        "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJwWXBrSFRHYnVmTndYRnpPZGQwMTRiSnU0ZFhzUk5qbUhmOXZHcUJDcXRrIn0.eyJleHAiOjE2OTQ2Nzg1MzUsImlhdCI6MTY5NDY3ODIzNSwianRpIjoiYzljN2MwNTktYWI5YS00ZjJlLTg0ZjItNmU2NzM0ODY3ZmVmIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDg4L2F1dGgvcmVhbG1zL2RyZG9fcmVhbG0iLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiMjA0MTEwNmUtNDliNi00OWUwLWJkN2QtOWJiYjRhZmFlNGY2IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2ViX2FwcCIsInNlc3Npb25fc3RhdGUiOiI5YTliZjVjZS05NzVkLTQyZDYtYWU0NS1kNjQyYmJhOTZlZDEiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMCJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsicmVndWxhcl91c2VyIiwic3VwZXJfYWRtaW4iLCJvZmZsaW5lX2FjY2VzcyIsImFkbWluIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI5YTliZjVjZS05NzVkLTQyZDYtYWU0NS1kNjQyYmJhOTZlZDEiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6ImNoYXJhbiIsImVtYWlsIjoic3JpY2hhcmFuQHNoeWVuYS5pbiJ9.IM6zRp2MCY0ByiUWzvlabReLMIYa1kMDOIODB-qAG8AHB1f5pfR8BnsTBg090q_d8Lk_FmybUn3OLd_XJpw-sgKZECfXyWP9024vwHklC3HDBqs4vtBE1Y4p06xg6OUPQGf2cTYxCjlgFy8SjVTOpMXuosZQ4DbCLZsP6hIsNXhjOFI5NZtwK-SOWMwyc9-BGY80l2bDusD60KL_sEp7EkJ5rjHD3dZsyH7p7KnBtKgPV8J7GeTunYCCclCw1P-xYz_zT1o4c-oFDcVUalXYBP44KCmoQTBVOJCFTcOxQ64FZ1i8lIFv2la0LQWNNt4QfT1Co6yc7ELx2P-CftwB6A"
    }
    
    # Decode Token
    KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
    options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
    token_info = keycloak_openid.decode_token(token['access_token'], key=KEYCLOAK_PUBLIC_KEY, options=options)

    print(token_info)

    

    return HttpResponse("Hello")

def secured_hello(request):
    return HttpResponse("Secured Hello")