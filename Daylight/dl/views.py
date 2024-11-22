from django.shortcuts import render,HttpResponse,HttpResponseRedirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.files.storage import default_storage
from datetime import time
from datetime import datetime
from django.shortcuts import render
from django.utils import timezone
from .models import *

def index(request) :

    # 오늘 날짜 구하기
    today = timezone.now().date()

    # 오늘 날짜에 해당하는 Todo 항목만 가져옴
    todos = Todo.objects.filter(done=False, time__date=today)
    done_todos = Todo.objects.filter(done=True, time__date=today)

    # 템플릿에 전달할 데이터
    content = {'todos': todos, 'done_todos': done_todos}

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

     # time 값이 있을 경우 datetime 객체로 변환
    if todo_time_str:  # todo_time_str이 빈 문자열이 아니면
        # 오늘 날짜와 받아온 시간 합치기
        date_str = datetime.now().date()  # 오늘 날짜
        time_obj = datetime.combine(date_str, datetime.strptime(todo_time_str, '%H:%M').time())
    else:
        time_obj = None  # time 값이 없으면 None 처리

    new_todo = Todo(content=todo_content, text_content=todo_text, time=time_obj)
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
    todos = Todo.objects.filter(done=False)  # 완료되지 않은 항목들만 가져옴
    done_todos = Todo.objects.filter(done=True)
    content = {'todos': todos,'done_todos': done_todos}
    return render(request, 'Table/timesheet.html', content)

def main(request) :
    return HttpResponseRedirect(reverse('index'))

def loginsheet(request) :
    return render(request,'Table/login.html')


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
        star_del.delete()

    return HttpResponseRedirect(reverse('starpage'))  


def sharedpage(request):
    todos = Todo.objects.all()
    content = {'todos': todos}
    return render(request, 'Table/sharedPage.html', content)