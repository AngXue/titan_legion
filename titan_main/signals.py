import os
from urllib.parse import urlparse, unquote

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Item
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(pre_delete, sender=Item)
def delete_item_image(sender, instance, **kwargs):
    if instance.item_image:
        # 解析图片URL
        parsed_url = urlparse(instance.item_image)
        # 解码URL路径
        decoded_path = unquote(parsed_url.path)
        # 获取MEDIA_ROOT
        media_root = settings.MEDIA_ROOT
        # 如果路径以MEDIA_URL开头，则去除前缀
        if decoded_path.startswith(settings.MEDIA_URL):
            decoded_path = decoded_path[len(settings.MEDIA_URL):]
        # 构建图片路径
        image_path = os.path.join(media_root, decoded_path.lstrip('/'))
        if os.path.isfile(image_path):
            os.remove(image_path)


@receiver(pre_save, sender=Item)
def update_item_image(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_item = Item.objects.get(pk=instance.pk)
    except Item.DoesNotExist:
        return

    old_image_url = old_item.item_image
    new_image_url = instance.item_image

    if old_image_url and old_image_url != new_image_url:
        parsed_old_url = urlparse(old_image_url)
        decoded_old_path = unquote(parsed_old_url.path)
        media_root = settings.MEDIA_ROOT
        if decoded_old_path.startswith(settings.MEDIA_URL):
            decoded_old_path = decoded_old_path[len(settings.MEDIA_URL):]
        old_image_path = os.path.join(media_root, decoded_old_path.lstrip('/'))
        if os.path.isfile(old_image_path):
            os.remove(old_image_path)
