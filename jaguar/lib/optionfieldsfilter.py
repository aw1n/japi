from rest_framework import serializers

class OptionFieldsFilter(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.custom_validation(kwargs)

        # Instantiate the superclass normally
        super(OptionFieldsFilter, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        unit = self.context.get('unit', None)

        if unit:
            self.fields.pop(unit)

        if request:
            opt_fields = request.query_params.get('opt_fields', None)
            if opt_fields:
                opt_fields = opt_fields.split(',')
                # Remove not specified fields
                to_show = set(opt_fields)
                default = set(self.fields.keys())
                for field in default - to_show:
                    self.fields.pop(field)

    def custom_validation(self, kwargs):
        try:
            if not kwargs['data']['birthday']:
                kwargs['data']['birthday'] = None
        except:
            pass