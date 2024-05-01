from django import forms
from main.models import UserProfile


class UserProfileChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'style': 'width: 50%;'})

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'expected_salary_range', 'experience', 'contact_info', 'resume')


class UserProfilePictureChangeForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = UserProfile
        fields = ("profile_picture",)
