from django import forms
from .models import Challenges
from django import forms
from .models import Users

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Users
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
class challengeForm(forms.ModelForm):
    class Meta:
        model = Challenges
        fields = ('challenge_title', 'created_username', 'challenge_content', 'board',
                  'created_date', 'start_date','end_date', 'duration')

        labels = {
            'challenge_title' : '챌린지 이름',
            'created_username' : '작성자명',
            'challenge_content' : '챌린지내용',
            'board' : '장/단기 선택',
            'created_date' : '챌린지 생성일',
            'start_date' : '시작일',
            'end_date' : '종료일',
            'duration' : '기간'
        }
