import pdb
import requests

SERVER = "http://0.0.0.0:8000"

def test_health():
    answer = requests.get(SERVER)
    assert answer.status_code==200

    
if __name__=="__main__":
    test_health() 