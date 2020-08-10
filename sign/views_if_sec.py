import hashlib

import time

from django.contrib import auth as django_auth
import base64

#用户认证
from django.http import JsonResponse


def user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION',b'')
    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1].decode('utf-8').partition(':'))
    except IndexError:
        return 'null'
    username ,password = auth_parts[0],auth_parts[2]
    user = django_auth.authenticate(username=username,password=password)
    if user is not None:
        django_auth.login(request,user)
        return 'success'
    else:
        return 'fail'

#查询发布会接口---增加用户认证
def get_event_list(request):
    auth_result = user_auth(request)#调用认证函数
    if auth_result == 'null':
        return JsonResponse({'status':10012,'message':'user auth fail'})
    eid = request.GET.get('eid','')#发布会id
    name = request.GET.get('name','')#发布会名称


#用户签名+时间戳
def user_sign(request):
    if request.method == 'POST':
        client_time = request.POST.get('time','')#客户端时间戳
        client_sign = request.POST.get('sign','')#客户端签名
    else:
        return 'error'

    if client_time == '' or client_sign == '':
        return 'sign null'

    #服务器时间
    now_time = time.time()
    server_time = str(now_time).split('.')[0]
    #获取时间差
    time_difference = int(server_time) - int(client_time)
    if time_difference >= 60:
        return 'time out'

    #签名检查
    md5 = hashlib.md5()
    sign_str = client_time + '&Guest-Bugmaster'
    sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()

    if server_sign != client_sign:
        return 'sign fail'
    else:
        return 'sign success'


#添加发布会接口--增加签名——时间戳

def add_event(request):
    sign_result = user_sign(request)
    if sign_result == 'error':
        return JsonResponse({'status':10011,'message':'request error'})
    elif sign_result == 'sign_null':
        return JsonResponse({'status':10012,'message':'user sign null'})
    elif sign_result == 'timeout':
        return JsonResponse({'status':10013,'message':'user sign timeout'})
    elif sign_result == 'sign fail':
        return JsonResponse({'status':10014,'message':'user sign error'})

