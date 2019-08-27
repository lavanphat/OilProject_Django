from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if username != '' and password != '':
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    # return HttpResponse('TÀI KHOẢN ĐÃ BỊ KHÓA')
                    messages.add_message(request, messages.WARNING, 'Tài khoản đã bị khóa')
            else:
                print('thử lại')
                print('user {} pass {}'.format(username, password))
                messages.add_message(request, messages.WARNING, 'Sai tên tài khoản hoặc mật khẩu')
                return HttpResponseRedirect(reverse('login'))
        else:
            messages.add_message(request, messages.WARNING, 'Chưa nhập username hoặc mật khẩu')
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required
def home(request):
    return render(request, 'home.html')

