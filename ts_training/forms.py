# Import
# #Global
import datetime
# #Django
from django import forms 
from django.urls import reverse
# #DB
from .models import Category, Training_spec, Person, Training_session, Planned_session


class DateInput(forms.DateInput):
		input_type = 'date'

class SessionForm(forms.ModelForm):
	# Model: Training_session. All of these fields are within this model.
	class Meta:
		model = Training_session
		fields = ['trainer', 'trainee', 'trainingId', 'date']
		labels = {
			'training_id': 'Training Points',
			'trainee': 'People Trained',
			'trainer': 'Trainer'
		}
		widgets = {
			'date': DateInput(),
			'trainingId': forms.CheckboxSelectMultiple(),
			'trainee': forms.CheckboxSelectMultiple(),
		}

	def clean(self):
		trainee = self.cleaned_data.get('trainee')
		training_id = self.cleaned_data.get('trainingId')
		trainer = self.cleaned_data.get('trainer')
		errors = {}
		# Can't submit without a valid trainer or date, so don't need to validate those.
		if trainee is None:
			errors['trainee'] = forms.ValidationError('Please select some trainees.')
		if training_id is None:
			errors['training_id'] = forms.ValidationError("You can't have a session without something to learn."
														  " Please select some training points.")
		if trainee is not None:
			if trainer in trainee.all():  # But the trainer should not be in the list of trainees.
				errors['trainer'] = forms.ValidationError("The trainer can't train themselves!")

		if errors:
			raise forms.ValidationError(errors)
			return self.cleaned_data
		
		# return self.cleaned_data

class PlanForm(forms.ModelForm):
	# Model: Planned_session. All of these fields are within this model.
	class Meta:
		model = Planned_session
		fields = ['trainer', 'trainingId', 'date', 'signed_up', 'slots']
		labels = {
			'trainingId': 'Training Points',
			'trainer': 'Trainer',
			'signed_up': 'Sign Up',
		}
		widgets = {
			'date': DateInput(),
			'trainingId': forms.CheckboxSelectMultiple(),
			'signed_up': forms.CheckboxSelectMultiple(),
		}

	def __init__(self, *args, **kwargs):
		super(PlanForm, self).__init__(*args, **kwargs)
		self.fields['signed_up'].required = False

	def clean(self):
		training_id = self.cleaned_data.get('trainingId')
		trainer = self.cleaned_data.get('trainer')
		errors = {}
		# Can't submit without a valid trainer or date, so don't need to validate those.
		if training_id is None:
			errors['training_id'] = forms.ValidationError("You can't have a session without something to learn."
														  " Please select some training points.")

		if errors:
			raise forms.ValidationError(errors)
			return self.cleaned_data
		
		# return self.cleaned_data

class SignupForm(forms.ModelForm):

	class Meta:
		model = Planned_session
		fields = ['signed_up', 'slots']
		widgets = {
			'signed_up': forms.CheckboxSelectMultiple(),
		}
	
	slots = forms.IntegerField(widget=forms.HiddenInput, required=False)

	def clean(self):
		cleaned_data = super(SignupForm, self).clean()
		self.instance.slots = self.instance.slots - 1
		return cleaned_data