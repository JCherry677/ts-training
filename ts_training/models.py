import datetime

from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# TechSoc Training Models


# Icon Model
class Icon(models.Model):
    itemType = models.CharField(
        max_length=15,
        verbose_name="Item Type",
        choices=(
            ('PAGE', 'Page'),
            ('CAT', 'Training Category'),
        ),
    )
    iconRef = models.CharField(
        max_length=25,
        verbose_name="Font Awesome Icon for Item"
    )
    iconRef.short_description = "Icon Code"
    iconName = models.CharField(max_length=25,
                                verbose_name="Item Name")
    weight = models.IntegerField(verbose_name="Item Number")
    primary = models.BooleanField(default=False)
    description = models.TextField(
        null=True,
        blank=True,
    )
    viewName = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        if self.itemType == 'PAGE':
            return self.iconName  # + ' (' + str(self.weight) + ')'
        elif self.itemType == 'CAT':
            return str(self.weight) + '. ' + self.iconName

#Manager class to work with Person class
class PersonManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and Saves a User with given email, 
        first and last name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and Saves a superuser with given email, 
        first and last name and password.
        """
        user = self.create_user(
            email,
            password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Person / Member of the Society - Is now login details too
#Is a custom User model based on the AbstractBaseUser Model
class Person(AbstractBaseUser):
    #Person fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    grad_year = models.IntegerField(null=True, blank=True,)
    committee = models.BooleanField(default=False)

    status = models.CharField(
        max_length=15,
        choices =(
            ('GRAD', 'Graduated'),
            ('STU', 'Student'),
            ('UNKNOWN', 'Unknown')
        ),
        null = False,
        default='UNKNOWN'
    )
    slug = models.SlugField(
        max_length=100,
        null = True,
        unique = True,
    )
    slug.short_description = "Name"

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    #Get methods from personManager
    objects = PersonManager()

    #Username is email address
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.get_full_name()

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

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def get_short_name(self):
        return self.first_name


# Training Specification
class Training_spec(models.Model):
    trainingId = models.DecimalField(
        verbose_name="Spec ID Number",
        max_digits = 4,
        decimal_places = 2,
        unique = True,
    )
    category = models.ForeignKey(Icon,
        limit_choices_to={'itemType': 'CAT'}, on_delete=models.CASCADE)
    trainingTitle = models.CharField(verbose_name="Training Title",
                                     max_length=50)
    description = models.TextField(default="Provide a useful description")
    safety = models.BooleanField(default=False)

    def __str__(self):
        humanTitle = str(self.trainingId) + ' - ' + self.trainingTitle
        return humanTitle


Training_spec.short_description = "Training Specification"


# Training Sessions
class Training_session(models.Model):
    trainingId = models.ManyToManyField(Training_spec)
    trainer = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="trainer")
    trainee = models.ManyToManyField(Person, related_name="trainee")
    date = models.DateField(
        default = datetime.date.today
    )

    def __str__(self):
        trainees = []
        for person in self.trainee.all():
            name = str.title(person.first_name) + ' ' + (str.title(person.last_name))
            trainees.append(name)
        string = str.title(self.trainer.first_name + ' ' + self.trainer.last_name) + ' taught ' \
                 + ', '.join(map(str, trainees))
        return string

    def get_absolute_url(self):
     	return reverse('ts_training:ntSessions', kwargs={'pk': self.pk})

    def get_students(self):
        return self.trainee.all().filter(status='STU')

#Planned Session
class Planned_session(models.Model):
    trainingId = models.ManyToManyField(Training_spec)
    trainer = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    slots = models.IntegerField(default=0, verbose_name="Available Slots")
    date = models.DateTimeField(
        default = timezone.now
    )
    signed_up = models.ManyToManyField(Person, related_name="signed_up", blank=True)

    def __str__(self):
        words = 'Session has '+ str(self.slots)  + ' slots available on ' + str(self.date)
        return words
    
