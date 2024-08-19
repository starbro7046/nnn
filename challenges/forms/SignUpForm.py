
from django import forms
from ..models import UsersModel

class SignUpForm(forms.ModelForm):
    class Meta:
        model = UsersModel
        fields = ['username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput(),  # 비밀번호 입력 시 숨김 처리
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = forms.PasswordInput().render(name='password', value=user.password)
        if commit:
            user.save()
        return user