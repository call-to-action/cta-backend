from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from taggit.managers import TaggableManager
# Create your models here.

class CtaUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

	def create_superuser(self, email, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(email,password=password,)
		user.is_admin = True
		user.save(using=self._db)
        return user


class CtaUser(AbstractBaseUser):
	email = models.EmailField(max_length=255,unique=True)
	name = models.CharField(max_length=200)
	is_activity_public = models.BooleanField(default=True)
	is_verified = models.BooleanField(default=False)
	is_organization =  models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	created_at = models.DateTimeField(default=timezone.now())
	updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    
	objects = CtaUserManager()

	USERNAME_FIELD = 'email'

	def get_full_name(self):
	    # The user is identified by their email address
	    return self.email

	def get_short_name(self):
	    # The user is identified by their email address
	    return self.email

	def __str__(self):              # __unicode__ on Python 2
	    return self.email

	def has_perm(self, perm, obj=None):
	    "Does the user have a specific permission?"
	    # Simplest possible answer: Yes, always
	    return True

	def has_module_perms(self, app_label):
	    "Does the user have permissions to view the app `app_label`?"
	    # Simplest possible answer: Yes, always
	    return True

	@property
	def is_staff(self):
	    "Is the user a member of staff?"
	    # Simplest possible answer: All admins are staff
	    return self.is_admin

class CallToAction(models.Model):
	#phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	created_by = models.ForeignKey(CtaUser)
	title = models.CharField(max_length=200)
	description = models.TextField()
	action_item = models.TextField()
	phone = models.CharField(max_length=25)
	tags = TaggableManager()
	created_at = models.DateTimeField(default=timezone.now())
	updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)


	def __str__(self):
		return "%s,%s,%s" % (what,phone,str(created_at)[:10])
		 
	class Meta:
		verbose_name = "Call To Action"
		verbose_name_plural = "Call To Actions"


#I am intentially making this not normalized 
class UserCallToAction(models.Model):
	REJECTED = 0
	ACCEPTED = 1
	BOOKMARKED = 2
	STATUS_OPTIONS = (
	    (REJECTED, 'REJECTED'),
		(ACCEPTED, 'ACCEPTED'),
		(BOOKMARKED, 'BOOKMARKED'),
	)

	user = models.ForeignKey(CtaUser)
	cta = models.CharField(max_length=200)
	status =models.IntegerField(choices=STATUS_OPTIONS)
	created_at = models.DateTimeField(default=timezone.now())
	updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)	
	
	def __str__(self):
		return "YES %s %s" % (user,cta)
		 
	class Meta:
		verbose_name = "User Call To Action"
		verbose_name_plural = "User Call To Actions"


class UserSubcriptionManager(models.Manager):
    """
    Custom manager for :model:'cta.UserSubcription'
    """

    def subscribers(self, user):
        return self.get_queryset().filter(subscription=user)

    def suscriptions(self, user):
        return self.get_queryset().filter(subscriber=user)

class UserSubscription(models.Model):
	"""
	Stores relation between a subscriber and the one being subscribed and vice versa

	related to :model:'cta.CtaUser'
	"""
	BLOCK = 0
	ALLOW = 1	
	STATUS_OPTIONS = (
	    (ALLOW, 'ALLOW'),
		(BLOCK, 'BLOCK'),
	)
	subscriber = models.ForeignKey(CtaUser, related_name="user_subscriber")
	subscription = models.ForeignKey(CtaUser, related_name="user_subscription")
	status =models.IntegerField(choices=STATUS_OPTIONS)
	created_at = models.DateTimeField(default=timezone.now())
	updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)	
	objects = UserSubcriptionManager()

	def __unicode__(self):
	    return "%s -> %s" % (self.subscribers.username, self.subscriptions.username)

	class Meta:
	    verbose_name = "User Subscription"
	    verbose_name_plural = "User Subscriptions"

