class YunPian(object):
    def __init__(self,api_key):
        self.api_key=api_key
        self.single_send_url='https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self,mobile,code):
        