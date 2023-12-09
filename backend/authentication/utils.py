from rest_framework.response import Response


def make_response(response: Response) -> Response:
    response.set_cookie(key='refresh', value=response.data.pop('refresh', "unknown"))
    return response
