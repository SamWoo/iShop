import xadmin
from user_operation.models import UserFav, UserLeavingMessag, UserAddress


class UserFavAdmin(object):
    list_display = ['user', 'goods', 'add_time']


class UserAddressAdmin(object):
    list_display = ["signer_name", "signer_mobile", "district", "address"]


class UserLeavingMessageAdmin(object):
    list_display = ['user', 'message_type', 'message', 'add_time']


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserLeavingMessag, UserLeavingMessageAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
