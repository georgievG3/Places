
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ListingImageFileSizeValidator:

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