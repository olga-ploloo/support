from user.models import User


def created_message_notification(instance):
    if instance.author.role == User.Role.CUSTOMER:
        print('is supp')
