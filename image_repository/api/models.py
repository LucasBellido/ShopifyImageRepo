import os
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db import models
from django.core.files import File  
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from urllib import request

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user



class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, null=False)
    username = models.CharField(max_length=30, unique=True, null=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
 
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = MyAccountManager()

    def __str__(self):
	    return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
	    return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
	    return True


class Image(models.Model):
    added_at = models.DateField(auto_now_add=True)
    private = models.BooleanField(null=False, default=False) 
    image = models.ImageField(upload_to='images/', null=True, blank=True) #change photo path if needed
    imageURL = models.URLField(default="", blank=True)
    favorites = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    user = models.ForeignKey(Account, on_delete=CASCADE)
    
    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.imageURL and not self.image:
            result = request.urlretrieve(self.imageURL)
            self.image.save(
                os.path.basename(self.imageURL),
                File(open(result[0], 'rb'))
                )
        super(Image, self).save(*args, **kwargs)

class Album(models.Model):
    name = models.CharField(unique=True, max_length=80, default="")
    description = models.TextField(default="")
    created_at = models.DateField(auto_now_add=True)
    private = models.BooleanField(null=False, default=False)
    users = models.ManyToManyField(Account)
    images = models.ManyToManyField(Image)
    

    def __str__(self):
        return str(self.pk)

