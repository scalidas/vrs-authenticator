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

		#Validate CSRF Token
		csrf_token_cookie = request.COOKIES.get('g_csrf_token')
		if not csrf_token_cookie:
			return HttpResponse("ERR_400: No CSRF Token in Cookie")
		csrf_token_body = request.POST.__getitem__('g_csrf_token')
		if not csrf_token_body:
			return HttpResponse("ERR_400: No CSRF Token in POST body")
		if csrf_token_cookie != csrf_token_body:
			return HttpResponse("ERR_400: Failed to verify double submit cookie")

		#Validate ID Token
		token = request.POST.__getitem__("credential")
		try:
			idinfo = id_token.verify_oauth2_token(token, requests.Request(), "1089272278877-rhnl6uenbnsk1gkuhu3jb7kedn2suto5.apps.googleusercontent.com")
			userid = idinfo['sub']
		except ValueError:
			# Invalid token
			return HttpResponse("Invalid JSON Web Token")

		try:
			user = GoogleUser.objects.get(sub=userid)
			user.logins = user.logins+1
			user.save()
		except:
			user = GoogleUser(sub=userid, logins=1)
			user.save()

		sessionid = get_random_string()
		newsession = CustomSession(sessionid=sessionid, user=user)
		newsession.expiry = datetime.datetime.now() + datetime.timedelta(days=0.5)
		newsession.save()

		return HttpResponse("It worked")





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