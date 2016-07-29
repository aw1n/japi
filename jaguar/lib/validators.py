from rest_framework.exceptions import ValidationError
from rest_framework.utils.representation import smart_repr
from rest_framework.compat import unicode_to_repr


missing_message = ('This field is required')

class RequiredFieldValidator(object):

    @staticmethod
    def validate(data, fields):
        missing = dict([
            (field_name, missing_message)
            for field_name in fields
            if field_name not in data
            ])
        if missing:
            raise ValidationError(missing)