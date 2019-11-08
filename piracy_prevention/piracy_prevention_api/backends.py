from .models import UserProfile
import logging


class MyAuthBackend(object):
    def authenticate(self, email, password):    
        try:
            user = UserProfile.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except UserProfile.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists " %email)
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
            if user.is_active:
                return user
            return None
        except UserProfile.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None

def check_Validity():
    pass