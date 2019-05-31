import requests


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, mobile, code):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【iShop生鲜超市】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }

        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict

# for test
if __name__ == "__main__":
    yunpian=YunPian(api_key)
    ret=yunpian.send_sms(mobile='10086',code='1234')
    print(ret)
