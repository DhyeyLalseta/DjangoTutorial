from django import forms

from .models import Question, Choice


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ["question"]


ChoiceFormSet = forms.formset_factory(ChoiceForm, extra=3, min_num=1, validate_min=True)
