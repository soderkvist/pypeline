from flask import Flask, request
from dotenv import load_dotenv
import os
from hmac import HMAC, compare_digest
from hashlib import sha1
import subprocess

load_dotenv()

SECRET_TOKEN = os.getenv('SECRET_TOKEN')

app = Flask(__name__)

def verify_signature(req):
    try:
        request_signature = req.headers.get('X-Hub-Signature').split('sha1=')[-1].strip()
        signature = HMAC(key=SECRET_TOKEN.encode(), msg=req.data, digestmod=sha1).hexdigest()
        return compare_digest(request_signature, signature)
    except AttributeError:
        return False


def execute_order_sixty_six():
    subprocess.call("./deploy_script.sh", shell=True)
    print("All done (?)")


@app.route('/payload', methods=['POST'])
def payload():
    if True: # verify_signature(request):
        execute_order_sixty_six()

        return 'Successfully', 200
    return 'Forbidden', 403


