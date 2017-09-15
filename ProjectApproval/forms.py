from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
from ProjectApproval.models import Project


class AddActivityForm(ModelForm):
    activity_time_from = forms.DateField(label='活动开始时间',
                                         widget=SelectDateWidget())
    activity_time_to = forms.DateField(label='活动结束时间',
                                       widget=SelectDateWidget())

    class Meta:
        model = Project
        fields = ['title', 'workshop', 'activity_time_from',
                  'activity_time_to', 'site', 'form', 'charger',
                  'contact_info', 'activity_range', 'amount', 'has_social',
                  'budget', 'comment', 'instructor_comment',
                  'attachment']

class UpdateActivityForm(AddActivityForm):
    pass
