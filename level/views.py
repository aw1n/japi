from rest_framework import renderers, viewsets, mixins, status, filters, parsers
from rest_framework.response import Response
from django.core import serializers
from django.http import Http404
from django.db.models import Count
from level.serializers import LevelSerializer
from level.filters import LevelFilter
from level.models import Level
from jaguar.utils import ESPagination
from configsettings.models import Discount

import django_filters
import json
import ast
import collections


level_fields = [
                'name',
                'remit_limit',
                'online_limit',
                'withdraw_limit',
                'withdraw_fee',
                # 'withdraw_fee_way',
                'reg_present',
                'remit_check',
                'service_rate',
                'memo',
                'status',
                'cdt_deposit_num',
                'cdt_deposit_amount',
                'cdt_deposit_max',
                'cdt_withdraw_num',
                'cdt_withdraw_amount',
                ]

fields_to_convert = [
                    'remit_limit',
                    'online_limit',
                    'withdraw_limit',
                    'withdraw_fee',
                    'reg_present',
                    'remit_check',
                    ]


class LevelViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    '''
    @class LevelViewSet
    @brief
        View set for Level model
        Handles HTTP requests such as POST, GET, PUT
    '''

    queryset = Level.objects.all()
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = LevelSerializer
    filter_class = LevelFilter
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name', 'status')
    pagination_class = ESPagination


    def list(self, request):
        '''
        @fn list
        @brief
            Overrides the list method (GET). This also filters the queryset
            by the parameters given by the user
        '''

        try:
            levels = Level.objects.all()

            levels = self.filter_queryset(levels.annotate(member_count=Count('member_level', distinct=True)))
            paginated_level = self.paginate_queryset(levels)
            serializer = LevelSerializer(paginated_level,
                                            context={'request': request},
                                            many=True)

            to_display = list()
            for serialized_lvl in serializer.data:
                to_display.append(self.__convert_data_to_display(serialized_lvl))

            # return Response(to_display[start_idx:max_idx], status=status.HTTP_200_OK)
            return Response(to_display, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            raise Http404

    def retrieve(self, request, pk):
        '''
        @fn retrieve
        @brief
            Overrides the retrieve method, get specific item.
        '''

        level_dict = dict()

        try:
            level = Level.objects.get(pk=pk)
            serializer = LevelSerializer(level, context={'request': request})

            # Format data to display.
            to_display = self.__convert_data_to_display(serializer.data)

            return Response(to_display, status=status.HTTP_200_OK)
        except Exception as err:
            raise Http404

    def create(self, request):
        '''
        @fn create
        @brief
            Overrides the create (POST) method to handle the discount.
        '''

        level_dict = dict()
        response = dict()

        for field in level_fields:
            if request.data.get(field) is not None:
                level_dict[field] = request.data.get(field)

        remit_discount = request.data.get('remit_discounts')
        online_discount = request.data.get('online_discounts')

        try:
            level = Level(**level_dict)
            serializer = LevelSerializer(level, data=level_dict, context={'request': request})
            if not serializer.is_valid():
                response['error'] = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            if remit_discount:
                self.__create_update_discount(level.level_remit_discount, remit_discount)
            if online_discount:
                self.__create_update_discount(level.level_online_discount, online_discount)

            # Format data to display.
            to_display = self.__convert_data_to_display(serializer.data)

            return Response(to_display, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            response['error'] = str(err)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        '''
        @fn update
        @brief
            Overrides the update (PUT) method to handle the discount
        '''

        level_dict = dict()
        response = dict()

        for field in level_fields:
            if request.data.get(field) is not None:
                level_dict[field] = request.data.get(field)

        remit_discount = request.data.get('remit_discounts')
        online_discount = request.data.get('online_discounts')

        try:
            level = Level.objects.get(pk=pk)
            serializer = LevelSerializer(level, data=level_dict, context={'request': request})

            if not serializer.is_valid():
                response['error'] = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            if remit_discount:
                self.__create_update_discount(level.level_remit_discount, remit_discount)
            if online_discount:
                self.__create_update_discount(level.level_online_discount, online_discount)

            # Format data to display.
            to_display = self.__convert_data_to_display(serializer.data)

            return Response(to_display, status=status.HTTP_200_OK)
        except Exception as err:
            response['error'] = str(err)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def __create_update_discount(self, lv_discount_inst, discount_details={}):
        '''
        @fn __create_update_discount
        @brief
            Creates or updates discount details then adds the discount to the given level.
        '''

        # clear the relationship for the level discount instance
        lv_discount_inst.clear()
        # process new relationships

        for discount in discount_details:
            # check if every field exists
            vailded = [(key in discount and discount.get(key) != '' ) for key in ['rate', 'check_rate', 'threshold']]

            if False in vailded:
                continue

            # check if discout had id
            if not discount.get('id'):

                # create discount
                discount_inst = lv_discount_inst.create(**discount)
                discount_inst.save()
                continue

            # update existing discount
            to_update = Discount.objects.get(pk=discount.get('id'))

            for key, value in discount.iteritems():
                setattr(to_update, key, value)
            to_update.save()

            # add to level
            lv_discount_inst.add(to_update)
        return

    def __convert_data_to_display(self, data):
        '''
        @fn __convert_data_to_display
        @brief
            Converts the corresponding data to dictionary
        '''

        to_display = collections.OrderedDict()
        for key, val in data.iteritems():
            if key in fields_to_convert:
                val = collections.OrderedDict(ast.literal_eval(val))
            to_display[key] = val
        return to_display

    def __get_query_index(self, start, max_val):
        '''
        @fn __get_query_index
        @brief
            Returns the indeces for start and max
        '''

        max_idx = None
        start_idx = 0
        if start is not None:
            start_idx = int(start)
        if max_val is not None:
            max_idx = start_idx + int(max_val)
        return start_idx, max_idx
