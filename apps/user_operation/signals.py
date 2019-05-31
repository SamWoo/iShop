from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def create_fav(sender, instance=None, created=False, **kwargs):
    '添加一个商品收藏'
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_fav(sender, instance=None, created=False, **kwargs):
    '删除一个商品收藏'
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
