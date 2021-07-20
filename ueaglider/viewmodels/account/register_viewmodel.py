import os
import sys
import json
from ueaglider.services import user_service
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, folder)
with open(folder + '/ueaglider/secrets.txt') as json_file:
    secrets = json.load(json_file)


class RegisterViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.name = self.request_dict.name
        self.email = self.request_dict.email.lower().strip()
        self.secret = self.request_dict.secret.lower().strip()
        self.password = self.request_dict.password.strip()
        self.age = self.request_dict.age.strip()

    def validate(self):
        if not self.name or not self.name.strip():
            self.error = 'You must specify a name.'
        elif not self.email or not self.email.strip():
            self.error = 'You must specify a email.'
        elif self.secret != secrets['magic_word']:
            self.error = "You didn't say the magic word"
        elif not self.password:
            self.error = 'You must specify a password.'
        elif len(self.password.strip()) < 8:
            self.error = 'The password must be at least 8 characters.'
        elif user_service.find_user_by_email(self.email):
            self.error = 'A user with that email address already exists.'
