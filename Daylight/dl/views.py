from django.shortcuts import render,HttpResponse,HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.files.storage import default_storage
from datetime import time
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from .models import *

def index(request) :

     # 오늘 날짜 계산
    today = timezone.now().date()

    # 이전 날짜와 다음 날짜 계산
    prev_date = today - timedelta(days=1)
    next_date = today + timedelta(days=1)

    # 전날 - 7일과 다음날 + 7일 범위 데이터 가져오기
    start_date = today - timedelta(days=7)
    end_date = today + timedelta(days=7)

    todos = Todo.objects.filter(done=False, time__date__range=(start_date, end_date))
    done_todos = Todo.objects.filter(done=True, time__date__range=(start_date, end_date))

    content = {
        'todos': todos,
        'done_todos': done_todos,
        'today': today,
        'prev_date': prev_date,  # 이전 날짜
        'next_date': next_date,  # 다음 날짜
    }

    # 'Table/main.html' 템플릿 렌더링
    return render(request, 'Table/main.html', content)


# 특정 날짜에 해당하는 Todo 항목을 JSON으로 반환
def todos_by_date(request, date_str):
     # 받은 날짜를 datetime 객체로 변환
    date_obj = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()

    # 해당 날짜의 할 일 목록만 필터링
    todos = Todo.objects.filter(done=False, date=date_obj)
    done_todos = Todo.objects.filter(done=True, date=date_obj)

    # 데이터를 JSON 형태로 반환
    todos_data = [{'content': todo.content, 'time': todo.time, 'text_content': todo.text_content, 'image': todo.image.url if todo.image else None, 'id': todo.id} for todo in todos]
    done_todos_data = [{'content': todo.content, 'time': todo.time, 'text_content': todo.text_content, 'image': todo.image.url if todo.image else None, 'id': todo.id} for todo in done_todos]

    return JsonResponse({'todos': todos_data, 'done_todos': done_todos_data})


def Create_todo(request) :
    todo_content = request.POST['todoTable']
    todo_text = request.POST['todoText']
    todo_time_str = request.POST.get('todoTime', '')  # 기본값을 빈 문자열로 설정

    
    today_date = datetime.now().date()  # 오늘 날짜

    if todo_time_str:
        try:
            time_part = datetime.strptime(todo_time_str, '%H:%M').time()  # 문자열을 time 객체로 변환
        except ValueError:
            time_part = time(0, 0)  # 잘못된 형식이면 기본값 00:00 설정
    else:
        time_part = time(0, 0)  # 시간 값이 비어 있으면 기본값 00:00 설정

    # 날짜와 시간을 합쳐 datetime 객체 생성
    datetime_obj = datetime.combine(today_date, time_part)


    new_todo = Todo(content=todo_content, text_content=todo_text, time=datetime_obj)
    new_todo.save()

    return HttpResponseRedirect(reverse('index'))

def Todo_delete(request) :
    done_todo_id = request.GET['todoNum']
    print("완료한 todo의 id", done_todo_id)
    todo = Todo.objects.get(id = done_todo_id)
  
    todo.delete()
    
    return HttpResponseRedirect(reverse('index'))

def Todo_update(request, todo_id) :
    todo = Todo.objects.get(id=todo_id)
    todos = Todo.objects.filter(done=False)
    content = {'todos':todos}
    return render(request, 'Table/updatePage.html', content)

def Update_todo(request) :
    todoId = request.POST['todoNum']
    change_todoTable = request.POST['todoTable']
    change_todoText = request.POST['todoText']

    before_todo = Todo.objects.get(id=todoId)
    before_todo.content = change_todoTable
    before_todo.text_content = change_todoText
    before_todo.save()

     # 해당 Todo와 동일한 content를 가진 Star_todo가 있는지 확인 후 업데이트
    
    return HttpResponseRedirect(reverse('index'))

def markStar(request) :
    star_id = request.POST['todo_id']
    star_todo = Todo.objects.get(id=star_id)
    star_todo.star = True
    star_todo.save()


    return HttpResponseRedirect(reverse('index'))   

def markDone(request) :
    todoId = request.POST['todo_id']
    done_todo = Todo.objects.get(id=todoId)
    done_todo.done = True
    done_todo.save()


    return HttpResponseRedirect(reverse('index'))   


def delete_done(request) :
    if request.method == "POST":
        # POST 요청으로 전송된 doneNum 값을 가져옴
        done_id = request.POST.get('doneNum')
            
        # 해당 ID를 가진 Todo 객체를 가져와서 삭제
        done_todo = get_object_or_404(Todo, id=done_id, done=True)
        done_todo.delete()

    return HttpResponseRedirect(reverse('index'))  


def update_modal(request) :
        todo_id = request.POST.get('todo_id', '').strip()  # 빈 공간 제거
        print(f'Todo ID received: "{todo_id}"')  # 확인 로그


        # todo_id를 숫자로 변환
        todo_id = int(todo_id)
        todo = get_object_or_404(Todo, id=todo_id)

        # 폼에서 넘어온 데이터를 사용하여 Todo 업데이트
        todo.content = request.POST.get('todoTable', '')  # 'todoTable'에서 'content'로 변경
        todo.text_content = request.POST.get('todoText', '')  # 'todoText'에서 'text'로 변경

         # 시간 업데이트 처리
        time_str = request.POST.get('todoTime')  # 시간 부분 (HH:MM)
        if time_str:
            print(f"Received time: {time_str}")  # 확인 로그
            try:
                date_str = datetime.now().date()  # 오늘 날짜 (YYYY-MM-DD)
                # 날짜와 시간을 결합하여 저장
                time_obj = datetime.combine(date_str, datetime.strptime(time_str, '%H:%M').time())
                todo.time = time_obj  # todo.time에 저장
            except ValueError as e:
                print(f"Error while parsing time: {e}")  # 예외 처리
                # 잘못된 형식이면 기본값으로 설정
                todo.time = datetime.now()



        # 파일이 업로드된 경우
        if request.FILES.get('todoImage'):
            image = request.FILES['todoImage']
            file_path = default_storage.save(f'media/todo_images/{image.name}', image)
            todo.image = file_path

        # 데이터 저장
        todo.save()
        print(f'Todo ID {todo_id} updated successfully')

        # 업데이트 후 index 페이지로 리디렉션
        return HttpResponseRedirect(reverse('index'))

    # POST가 아닌 요청에 대한 처리


def get_todos_by_date(request):
    date = request.GET.get('date')  # 요청에서 날짜 가져오기
    todos = Todo.objects.filter(date=date)  # 해당 날짜의 데이터 가져오기
    todos_data = [
        {
            "id": todo.id,
            "content": todo.content,
            "text_content": todo.text_content,
            "time": todo.time.strftime("%H:%M") if todo.time else "",
            "image": todo.image.url if todo.image else None
        }
        for todo in todos
    ]
    return JsonResponse({"todos": todos_data})




def search_view(request):
    query = request.GET.get('q', '')
     # 검색어에 해당하는 일반 Todo 항목 필터링
    todos = Todo.objects.filter(
        Q(content__icontains=query) | Q(text_content__icontains=query), done=False
    )
    # 검색어에 해당하는 완료된 Todo 항목 필터링
    done_todos = Todo.objects.filter(
        Q(content__icontains=query) | Q(text_content__icontains=query), done=True
    )
    return render(request, 'Table/search.html', {
        'todos': todos,
        'done_todos': done_todos,
        'query': query
    })



def timesheet(request):
     # 오늘 날짜 구하기
    today = timezone.now().date()

    # 오늘 날짜에 해당하는 Todo 항목만 가져옴
    todos = Todo.objects.filter(done=False, time__date=today)
    done_todos = Todo.objects.filter(done=True, time__date=today)

    # 템플릿에 전달할 데이터
    content = {'todos': todos, 'done_todos': done_todos}

    return render(request, 'Table/timesheet.html', content)

def main(request) :
    return HttpResponseRedirect(reverse('index'))

def loginsheet(request) :
    return render(request,'Table/login.html')


def join(request) :
    if request.method == "POST":
        email = request.POST.get('signupEmail', '').strip()
        pw = request.POST.get('signupPW', '').strip()
        print(email, pw)  # 디버그 출력 

        if not email or not pw:
            messages.error(request, "이메일과 비밀번호를 모두 입력해주세요.")
            return redirect('loginsheet')  # 로그인 페이지로 리다이렉트

        # 이미 존재하는 이메일 확인
        if User.objects.filter(user_email=email).exists():
            messages.error(request, "이미 등록된 이메일입니다.")
            return redirect('loginsheet')

        # 비밀번호 암호화 후 저장
        user = User(user_email=email, user_password=make_password(pw))
        user.save()

        # 성공 메시지와 로그인 페이지로 이동
        messages.success(request, '회원가입이 완료되었습니다.')
        return HttpResponseRedirect(reverse('loginsheet'))


def login_view(request):
    if request.method == 'POST':
        email = request.POST['signupEmail']
        pw = request.POST['signupPW']
        
        try:
            # 이메일로 사용자 찾기
            user = User.objects.get(user_email=email)
            
            # 비밀번호 검증
            if check_password(pw, user.user_password):
                # 비밀번호가 일치하면 세션에 사용자 이메일 저장
                request.session['signupEmail'] = user.user_email
                messages.success(request, '로그인 성공!')
                return HttpResponseRedirect(reverse('index'))  # 메인 페이지로 이동
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
                return HttpResponseRedirect(reverse('loginsheet'))  # 로그인 페이지로 이동
                
        except User.DoesNotExist:
            # 이메일이 존재하지 않으면 오류 메시지 표시
            messages.error(request, '존재하지 않는 이메일입니다.')
            return HttpResponseRedirect(reverse('loginsheet'))  # 로그인 페이지로 이동
    
    return HttpResponseRedirect(reverse('index'))  # 메인 페이지로 이동




def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            # Invalid login credentials
            return render(request, 'Table/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'Table/login.html')


def starpage(request):
    todos = Todo.objects.filter(star=True)
    content = {'todos': todos}
    return render(request, 'Table/starpage.html', content)


def delete_star(request) :
    if request.method == "POST":
        # POST 요청으로 전송된 doneNum 값을 가져옴
        star_id = request.POST.get('todo_id')
            
        # 해당 ID를 가진 Todo 객체를 가져와서 삭제
        star_del = get_object_or_404(Todo, id=star_id, star=True)
        star_del.star = False  # star 값을 False로 설정
        star_del.save()  # 변경사항 저장

        star_del.save()

    return HttpResponseRedirect(reverse('starpage'))  


def sharedpage(request):
    todos = Todo.objects.all()
    content = {'todos': todos}
    return render(request, 'Table/sharedPage.html', content)