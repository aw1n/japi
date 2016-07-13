from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import pagination
from collections import OrderedDict

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class ESPagination(pagination.LimitOffsetPagination):
    '''
    @class ESPagination
    @brief
        Handles the general parameters start and max
    '''

    def __init__(self, *args, **kwargs):
        '''
        @fn __init__
        @brief
            Overrides the attributes of parent class
        '''

        self.offset_query_param = 'start'
        self.limit_query_param = 'max'
        self.template = None
        self.limit_val = None
        self.off_val = None
        super(ESPagination, self).__init__(*args, **kwargs)

    def paginate_queryset(self, queryset, request, view=None):
        '''
        @fn paginate_queryset
        @brief
            Overriden method of the LimitOffsetPagination
            Paginate the queryset based on start and max general params
        '''

        self.off_val = request.query_params.get(self.offset_query_param)
        self.limit_val = request.query_params.get(self.limit_query_param)
        start_idx, max_idx = self.__get_query_index()

        return list(queryset[start_idx:max_idx])

    def get_paginated_response(self, data):
        '''
        @fn get_paginated_response
        @brief
            Overriden method of LimitOffsetPagination
            Get then return the paginated queryset
        '''
        
        return Response(data)

    def __get_query_index(self):
        '''
        @fn __get_query_index
        @brief
            Returns the indeces for start and max
        '''

        max_idx = None
        start_idx = 0
        if self.off_val is not None:
            start_idx = int(self.off_val)
        if self.limit_val is not None:
            max_idx = start_idx + int(self.limit_val)
        return start_idx, max_idx
