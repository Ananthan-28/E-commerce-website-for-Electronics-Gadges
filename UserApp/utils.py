import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
def product_rating(data):
    for i in data:
        if i.user_rating is None:
            i.user_rating = 0
            i.user_rating_half = False
        elif 2.5 <= ((i.user_rating * 10) % 10) <= 5:
            i.user_rating_half = True
            i.user_rating = int(i.user_rating)
        else:
            i.user_rating_half = False
    return data


def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(),interval=300)
    otp = totp.now()
    request.session['otp_key'] = totp.secret


    return otp
