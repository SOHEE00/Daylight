from django.shortcuts import render,HttpResponse,HttpResponseRedirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core.files.storage import default_storage
from .models import *

def index(request) :
    todos = Todo.objects.filter(done=False)  # 완료되지 않은 항목들만 가져옴
    done_todos = Todo.objects.filter(done=True)
    content = {'todos': todos, 'done_todos': done_todos}
    return render(request,'Table/main.html',content)

def Create_todo(request) :
    todo_content = request.POST['todoTable']
    todo_text = request.POST['todoText']
    new_todo = Todo(content = todo_content, text_content = todo_text)
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
    todos = Todo.objects.all()
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
        todo.content = request.POST.get('content', '')  # 'todoTable'에서 'content'로 변경
        todo.text_content = request.POST.get('text', '')  # 'todoText'에서 'text'로 변경

        # 파일이 업로드된 경우
        if request.FILES.get('todoImage'):
            image = request.FILES['todoImage']
            file_path = default_storage.save(f'todo_images/{image.name}', image)
            todo.image = file_path

        # 데이터 저장
        todo.save()
        print(f'Todo ID {todo_id} updated successfully')

        # 업데이트 후 index 페이지로 리디렉션
        return HttpResponseRedirect(reverse('index'))

    # POST가 아닌 요청에 대한 처리
    







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