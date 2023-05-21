from django.http import JsonResponse
from faker import Faker


def get_info(request):
    if request.method == "GET":
        fake = Faker(locale='zh_CN')
        return JsonResponse({'code': 200,
                             'data': {
                                 'name': fake.name(),
                                 'address': fake.address()
                             }
                             })
    return JsonResponse({'code': 500, 'msg': '不支持请求类型'})
