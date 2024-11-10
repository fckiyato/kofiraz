from kavenegar import *

def send_otp_code(phone, code):
    try:
        api = KavenegarAPI('55747979637A4255795544614A4B7868724F2B3852726F50366E73556332665554417A79313174694E71303D')
        params = {
            'sender':'',
            'receptor':phone,
            'message':f"سلام. به کوفیراز خوش آمدید. کد تایید احراز هویت شما عبارت است از: {code}",
        }
        responce = api.sms_send(params)
        print(responce)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)