import os
os.environ["SECRET_KEY"]="test-secret-key-123456789012345678901234567890"
from fastapi.testclient import TestClient
from app.main import app
from app.db import DB_PATH

client=TestClient(app)

def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='ok'

def test_auth_and_home():
    email='test@example.com'
    r=client.post('/api/auth/register',json={'name':'Test User','email':email,'password':'secret123'})
    assert r.status_code in (200,409)
    r=client.post('/api/auth/login',json={'email':email,'password':'secret123'})
    assert r.status_code==200
    token=r.json()['access_token']
    r=client.post('/api/generate-home',headers={'Authorization':f'Bearer {token}'},json={'budget':50000,'rooms':['Living Room'],'style':'modern','notes':''})
    assert r.status_code==200
    data=r.json(); assert data['planner']=='home'; assert len(data['recommendations'])>=1

def test_party_validation():
    r=client.post('/api/generate-party',json={'budget':0,'guests':10,'event_type':'birthday','venue':'home'})
    assert r.status_code==422
