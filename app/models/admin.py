from django.db import models
from .user import UserAccount

class AdminManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.type = UserAccount.Types.ADMIN
        user.is_admin = True
        user.save(using = self._db)
        return user
    
    def get_queryset(self , *args , **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.ADMIN)
        return queryset
    
class Admin(UserAccount):
    class Meta :
        proxy = True
    objects = AdminManager()
    
    def save(self  , *args , **kwargs):
        if not self.id or self.id == None : 
            self.type = UserAccount.Types.ADMIN
        return super().save(*args , **kwargs)
