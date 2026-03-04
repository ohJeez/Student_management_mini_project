from django import forms
from .models import Student, Feedback


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'roll_number', 'enrollment_date']
        widgets = {
            'first_name':      forms.TextInput(attrs={'placeholder': ' '}),
            'last_name':       forms.TextInput(attrs={'placeholder': ' '}),
            'email':           forms.EmailInput(attrs={'placeholder': ' '}),
            'roll_number':     forms.TextInput(attrs={'placeholder': ' '}),
            'enrollment_date': forms.DateInput(attrs={'placeholder': ' ', 'type': 'date'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'message', 'rating']
        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': ' ',
                'id': 'id_subject',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': ' ',
                'rows': 5,
                'id': 'id_message',
            }),
            'rating': forms.Select(attrs={
                'id': 'id_rating',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make rating optional with a blank first option
        self.fields['rating'].required = False
        self.fields['rating'].empty_label = "— No rating —"
        self.fields['rating'].widget.choices = [('', '— No rating —')] + [
            (i, f"{i} ★") for i in range(1, 6)
        ]
