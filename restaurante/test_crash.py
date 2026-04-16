import sys
import traceback
from django.test import Client
from django.contrib.auth.models import User

def check_urls():
    c = Client()
    user = User.objects.first()
    if user:
        c.force_login(user)
        print(f"Logged in as {user.username}")
    else:
        print("No user found!")
        
    urls = [
        '/', 
        '/productos/', 
        '/ordenes/', 
        '/ordenes/crear/',
        '/insumos/',
    ]
    for u in urls:
        try:
            r = c.get(u)
            print(f"{u}: {r.status_code}")
            if r.status_code == 500:
                print(r.content.decode('utf-8'))
        except Exception as e:
            print(f"CRASH on {u}:")
            traceback.print_exc()

check_urls()
