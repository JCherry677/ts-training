from django import forms
from django.db import models 
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from ts_training.models import Person

from .models import Icon, Person, Training_session, Training_spec, Planned_session

## This section deals with the custom User type
# User Forms
class PersonCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
    fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = Person
		fields = ('email', 'first_name', 'last_name')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class PersonChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Person
		fields = ('email', 'password', 'first_name', 'last_name', 'grad_year', 'committee', 'status', 'slug', 'is_active', 'is_admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]

#For displaying on the admin page
class PersonAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = PersonChangeForm
	add_form = PersonCreationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('email', 'first_name', 'last_name', 'grad_year', 'committee', 'is_admin')
	list_filter = ('status', 'grad_year', 'committee',)
	fieldsets = (
		(None, {'fields': ('email', 'password', 'slug')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'grad_year')}),
		('Society info', {'fields': ('status', 'committee',)}),
		('Permissions', {'fields': ('is_admin',)}),
	)
	
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2'),
		}),
	)

	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

##Other Admin Elements
class TrainingSpecAdmin(admin.ModelAdmin):
	list_filter = ['category']
	list_display = ['trainingId', 'category', 'trainingTitle', 'description', 'safety']

	def toggle_safety(modeladmin, request, queryset):
		for item in queryset:
			if not item.safety:
				# item.update(safety=True)
				setattr(item, 'safety', True)
				item.save()  
			elif item.safety:
				# item.update(safety=False)
				setattr(item, 'safety', False)
				item.save()

	actions = [toggle_safety]


class TrainingSessionAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'date', ]
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	}
	list_filter = ['date','trainee','trainer']


class IconAdmin(admin.ModelAdmin):
	prepopulated_fields = {"description": ("iconName",)}
	list_display = ['itemType', 'weight', 'iconName', 'iconRef']
	list_filter = ['itemType']

class PlannedAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'date', 'slots', ]
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	}
	list_filter = ['date']


admin.site.register(Person, PersonAdmin)
admin.site.register(Training_session, TrainingSessionAdmin)
admin.site.register(Training_spec, TrainingSpecAdmin)
admin.site.register(Icon, IconAdmin)
admin.site.register(Planned_session, PlannedAdmin)
#Groups are not needed due to custom User type
admin.site.unregister(Group)