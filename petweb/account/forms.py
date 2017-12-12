from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, UserManager, Pet, PetSpecies, PetBreed


# 사용자 생성 폼
class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일 주소',
                'required': 'True'
            }
        )
    )
    nickname = forms.CharField(
        label='Nickname',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '닉네임',
                'required': 'True'
            }
        )
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '패스워드',
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '패스워드 확인',
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('email', 'nickname')

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('패스워드가 일치하지 않습니다')
        return password2

    def save(self, commit=True):
        # 제공된 패스워드를 해쉬값으로 저장
        user = super(UserCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# 비밀번호 변경 폼
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label='Password'
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial['password']


# 펫 종류 수정 폼
class PetSpeciesChangeForm(forms.ModelForm):
    class Meta:
        model = PetSpecies
        fields = (
            'pet_type',
        )


# 펫 품종 수정 폼
class PetBreedChangeForm(forms.ModelForm):
    class Meta:
        model = PetBreed
        fields = (
            'species',
            'breeds_name',
        )


# 펫 수정 폼
class PetChangeForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = (
            'owner',
            'name',
            'birth_date',
            'species',
            'breeds',
            'body_color',
            'identified_number',
            'is_neutering',
            'is_active',
        )
