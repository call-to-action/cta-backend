from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
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
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CtaUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    name = models.CharField(max_length=200)
    is_activity_public = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_organization =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now())
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
	who = models.ForeignKey(CtaUser)
	what = models.CharField(max_length=200)
	why = models.CharField(max_length=200)
	how = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	tags = TaggableManager()
	pub_date = models.DateTimeField(default=timezone.now())

	def __str__(self):
		return "%s,%s,%s" % (what,phone,str(pub_date)[:10])
		 
	class Meta:
		verbose_name = "Accepted Cta"
		verbose_name_plural = "Accepted Cta"


#I am intentially making this not normalized 
class AcceptedCta(models.Model):
	user = models.ForeignKey(CtaUser)
	cta = models.CharField(max_length=200)
	pub_date = models.DateTimeField(default=timezone.now())
	def __str__(self):
		return "YES %s %s" % (user,cta)
		 
	class Meta:
		verbose_name = "Accepted Cta"
		verbose_name_plural = "Accepted Cta"


class RejectedCta(models.Model):
	user = models.ForeignKey(CtaUser)
	cta = models.CharField(max_length=200)
	pub_date = models.DateTimeField(default=timezone.now())

	def __str__(self):
		return "NO %s %s" % (user,cta)

	class Meta:
		verbose_name = "Rejected Cta"
		verbose_name_plural = "Rejected Cta"

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
    subscriber = models.ForeignKey(CtaUser, related_name="user_subscriber")
    subscription = models.ForeignKey(CtaUser, related_name="user_subscription")
    pub_date = models.DateTimeField(default=timezone.now())

    objects = UserSubscriberManager()

    def __unicode__(self):
        return "%s -> %s" % (self.subscribers.username, self.subscriptions.username)

    class Meta:
        verbose_name = "User Subscription"
        verbose_name_plural = "User Subscriptions"


class AcceptedCta(models.Model):
	user = models.ForeignKey(CtaUser)
	cta = models.CharField(max_length=200)
	pub_date = models.DateTimeField(default=timezone.now())
	def __str__(self):
		return "YES %s %s" % (user,cta)
		 
	class Meta:
		verbose_name = "Accepted Cta"
		verbose_name_plural = "Accepted Cta"
