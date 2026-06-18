from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Account

TEXT_INPUT = {
    'class': 'form-control',
}


class AccountAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(TEXT_INPUT)
        self.fields['password'].widget.attrs.update(TEXT_INPUT)


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(TEXT_INPUT)
