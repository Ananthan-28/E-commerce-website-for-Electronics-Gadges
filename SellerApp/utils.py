import pyotp
from datetime import datetime, timedelta
def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(),interval=300)
    otp = totp.now()
    request.session['otp_key'] = totp.secret

    return otp
