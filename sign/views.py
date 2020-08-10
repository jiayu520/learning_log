import logging

from django.contrib import auth
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
# def index(request):
#     return HttpResponse("Hello Django! ")
def index(request):
    return render(request,"index.html")

#登录操作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        # if username == 'admin' and password == 'admin123':
        #     #return HttpResponseRedirect('/event_manage')
        #     response = HttpResponseRedirect('/event_manage/')
        #     #response.set_cookie('user',username,3600)#添加浏览器cookie
        #     request.session['user'] = username#将seesion信息记录到浏览器
        #     return response
        # else:
        #     return render(request,'index.html', {'error': 'username or password error!'})
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)#登录
            request.session['user'] = username#将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})
#发布会管理
@login_required()
def event_manage(request):
    #username = request.COOKIES.get('user','')#读取浏览器cookie
    event_list = Event.objects.all()
    username = request.session.get('user','')#读取浏览器session
    return render(request,"event_manage.html",{"user": username,"events": event_list})

#发布会名称搜索
@login_required()
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return  render(request,'event_manage.html',{'user':username,'events':event_list})




@login_required()
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()
    paginator =Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html", {"user": username,"guests": contacts})


@login_required()
def search_user(request):
    username = request.session.get('user','')
    search_user = request.GET.get('guest','')
    user_list = Event.objects.filter(guest__contains=search_user)
    return render(request,'guest_manage.html',{'user':username,'guests':user_list})

@login_required
#签到视图
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    return render(request,'sign_index.html',{'event':event})

#签到动作
@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid)
    phone = request.POST.get('phone','')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error.'})
    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'event id or phone error.'})
    result = Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result})

@login_required
def logout(request):
    auth.logout(request)#退出登录
    response = HttpResponseRedirect('/index/')
    return response



