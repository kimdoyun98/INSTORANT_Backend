import jwt
from django.http import JsonResponse
from Sign.models import UserInfomation


# Token 인증
def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user_id = UserInfomation.objects.get(username=payload['username'])
            request.user = user_id

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID TOKEN'}, status=400)

        except UserInfomation.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER'}, status=400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper