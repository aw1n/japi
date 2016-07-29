from rest_framework import serializers

from account.models import Member
from .models import RemitInfo, Transaction, TransactionType
from jaguar.lib.validators import RequiredFieldValidator


class RemitInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemitInfo


class TransactionSerializer(serializers.ModelSerializer):
    remit_info = RemitInfoSerializer(required=False)
    member = serializers.PrimaryKeyRelatedField(required=False, queryset=Member.objects.all())
    transaction_type = serializers.PrimaryKeyRelatedField(required=False, queryset=TransactionType.objects.all())

    class Meta:
        model = Transaction
        # fields = ('remit_info',)

    def create(self, validated_data):
        remit_info = validated_data.pop('remit_info', None)
        print validated_data
        return validated_data

# class RemitInfoSerializer(serializers.ModelSerializer):
#     transaction = TransactionSerializer(required=False, many=True)

#     class Meta:
#         model = RemitInfo
#         # fields = ('bank', 'depositor', 'transaction')

#     def update(self, instance, validated_data):
#         for key, val in validated_data.items():
#             setattr(instance, key, validated_data[key])
#         instance.save()
#         return instance

#     def create(self, validated_data):
#         # print validated_data
#         remit_info = RemitInfo.objects.create(**validated_data)
#         if remit_info:
#             # status = 3 #ongoing
#             # transaction_type = 1 #remit
#             transaction = Transaction.objects.create(remit_info=remit_info)

#         return remit_info

#     def validate(self,data):
#         print data
#         request = self.context['request']

#         if request.method == 'POST':
#             RequiredFieldValidator.validate(data, ('bank', 'depositor'))
#         return data

    # def to_representation(self, obj):
    #     ret = super(RemitInfoSerializer, self).to_representation(obj)
    #     return {
    #         'transaction': obj.transaction_remit_info.values(),
    #         'remit_info': ret
    #     }