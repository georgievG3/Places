import datetime

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def validate_age(value):
    today = datetime.date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 18:
        raise ValidationError('Трябва да имате навършени 18 години.')


def name_validator_only_letters(value):
    allowed_chars = "-"

    for char in value:
        if not (char.isalpha() or char in allowed_chars):
            raise ValidationError("Името трябва да съдържа само букви и тирета.")


@deconstructible
class ProfilePictureFileSizeValidator:

    def __init__(self, file_size_limit, message=None):
        self.file_size_limit = file_size_limit
        self.message = message

    @property
    def message(self):
        return self.__message
    
    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"Размера на снимката трябва да е по-малък от {self.file_size_limit}MB."
        else:
            self.__message = value

    def __call__(self, value):
        if value.size > self.file_size_limit * 1024 * 1024:
            raise ValidationError(self.message)
