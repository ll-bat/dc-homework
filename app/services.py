import json
from json import JSONDecodeError

import requests
from django.core.serializers.json import DjangoJSONEncoder

from dc_assignment.settings import GOOGLE_API_TOKEN


class GoogleBookApiService:
    API_URL = "https://www.googleapis.com/books/v1/volumes"

    @classmethod
    def get_book_by_isbn(cls, isbn):
        payload = {
            'q': 'isbn:{}'.format(isbn),
            'key': GOOGLE_API_TOKEN,
        }

        try:
            response = requests.get(cls.API_URL, payload)
        except requests.exceptions.RequestException:
            return {
                'ok': False,
                'error_message': "Can't connect to book api to fetch metadata. Please, try again",
                'data': None
            }

        try:
            json_data = json.loads(response.content)
        except JSONDecodeError as e:
            return {
                'ok': False,
                'error_message': "Can't fetch book info. Please, try again",
                'data': None
            }

        book = None
        error_message = None
        if response.ok:
            books_with_extra_data = json_data.get('items', [])
            if len(books_with_extra_data):
                book = books_with_extra_data[0].get('volumeInfo', None)
            else:
                # book will be None, meaning that such book does not exist
                pass
        else:
            error_message = json_data.get('error', {}).get('message', "Can't fetch book info. Please, try again")

        return {
            'ok': response.ok,
            'data': book,
            'error_message': error_message,
        }
