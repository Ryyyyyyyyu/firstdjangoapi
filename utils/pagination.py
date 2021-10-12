# -*- coding: UTF-8 -*-
from rest_framework.pagination import PageNumberPagination as _PageNumberPagination


class PageNumberPagination(_PageNumberPagination):
    """
    A simple page number based style that supports page numbers as
    query parameters. For example:

    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&page_size=100
    """
    # The default page size.
    # Defaults to `None`, meaning pagination is disabled.
    page_size = 5

    # Client can control the page using this query parameter.
    page_query_param = 'page'
    page_query_description = 'A page number within the paginated result set.'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = 'page_size'
    page_size_query_description = 'Number of results to return per page.'

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 50

    invalid_page_message = 'Invalid page.'

