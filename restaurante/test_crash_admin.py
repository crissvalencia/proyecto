import sys
import traceback
from django.test import Client
from django.contrib.auth.models import User

def check_urls():
    c = Client()
    user = User.objects.filter(is_superuser=True).first()
    if user:
        c.force_login(user)
        print(f"Logged in as {user.username} (superuser)")
    else:
        print("No superuser found!")
        
    urls = [
        '/admin/', 
        '/admin/gestion/producto/',
        '/admin/gestion/insumo/',
        '/admin/gestion/orden/',
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
