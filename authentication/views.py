from django.http import HttpResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import GoogleUser, CustomSession
import random
import hashlib
import datetime
import time
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#View to handle authentication through google
@csrf_exempt
def g_authenticate(request):	
	
	if (request.method=='GET'):
		return HttpResponse("This page is meant to consume credentials...")

	if (request.method=='POST'):
		print(str(request.headers))

		#Get JWT
		token = request.body

		try:
    		# Specify the CLIENT_ID of the app that accesses the backend:
			idinfo = id_token.verify_oauth2_token(token, requests.Request(), "1089272278877-rhnl6uenbnsk1gkuhu3jb7kedn2suto5.apps.googleusercontent.com")

			# Or, if multiple clients access the backend server:
			# idinfo = id_token.verify_oauth2_token(token, requests.Request())
			# if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
			#     raise ValueError('Could not verify audience.')

			# If auth request is from a G Suite domain:
			# if idinfo['hd'] != GSUITE_DOMAIN_NAME:
			#     raise ValueError('Wrong hosted domain.')

			# ID token is valid. Get the user's Google Account ID from the decoded token.
			userid = idinfo['sub']
		except ValueError:
			# Invalid token
			return HttpResponse("Invalid JSON Web Token")

		# sessionid = get_random_string()
		# newsession = CustomSession(sessionid=sessionid)
		# newsession.expiry = datetime.now() + datetime.timedelta(days=0.5)
		# newsession.save()




def get_random_string(length=12,
	allowed_chars='abcdefghijklmnopqrstuvwxyz'
					'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
	"""
	Returns a securely generated random string.
	The default length of 12 with the a-z, A-Z, 0-9 character set returns
	a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
	"""
	random.seed(
		hashlib.sha256(
			("%s%s%s" % (
				random.getstate(),
				time.time(),
				settings.SECRET_KEY)).encode('utf-8')
		).digest())
	return ''.join(random.choice(allowed_chars) for i in range(length))