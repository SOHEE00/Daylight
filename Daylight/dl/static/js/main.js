// 디버깅을 위한 로그 함수
function log(message) {
    console.log(`[Debug] ${message}`);
}

// 모달 관련 전역 변수
var currentModal = null;

// todoTable, todoText, 또는 todoimg 클릭 시 모달 띄우기
document.querySelectorAll('.table-box2').forEach(function(tableBox2) {
    var clickableElements = tableBox2.querySelectorAll('input[id^="todoTable"], input[id^="todoText"], img[id^="todoimg"]');
    clickableElements.forEach(function(element) {
        element.onclick = function(event) { 
            event.preventDefault();
            openModal(tableBox2); 
        };
    });
});

function openModal(tableBox2) {
    log('Opening modal for table-box2');
    
    var todoId = tableBox2.querySelector('input[id^="todoNum"]')?.value;
    if (!todoId) {
        log('Todo ID not found');
        return;
    }
    log(`Todo ID: ${todoId}`);

    // 모달 찾기 (여러 가능한 ID 형식을 시도)
    currentModal = document.getElementById(`myModal${todoId}`) || 
                   document.querySelector(`[id^="myModal"][id$="${todoId}"]`) ||
                   document.querySelector(`#myModal-${todoId}`) ||  // 새로운 형식 추가
                   document.querySelector('.modal'); // 마지막 시도: 첫 번째 모달 선택
    
    if (!currentModal) {
        log(`Modal not found for ID: ${todoId}`);
        return;
    }
    log('Modal found');

    // 모달 내용 업데이트
    updateModalContent(tableBox2, todoId);

    // 모달 보이기
    currentModal.style.display = "block";
    log('Modal displayed');
}

function updateModalContent(tableBox2, todoId) {
    log(`Todo ID____: ${todoId}`);
    var todoContent = tableBox2.querySelector('input[id^="todoTable"]')?.value || '';
    var todoText = tableBox2.querySelector('input[id^="todoText"]')?.value || '';
    var todoImage = tableBox2.querySelector('img[id^="todoimg"]')?.src;

    console.log('todoImage___:', todoImage);

   

    var editTodoTable = currentModal.querySelector(`[id^="editTodoTable"][id$="${todoId}"]`) || currentModal.querySelector('[id^="editTodoTable"]');
    var editTodoText = currentModal.querySelector(`[id^="editTodoText"][id$="${todoId}"]`) || currentModal.querySelector('[id^="editTodoText"]');
   
    var editTodoImage = currentModal.querySelector(`[id^="editTodoImage"][id$="${todoId}"]`) || currentModal.querySelector('[id^="editTodoText"]');
    var editTodoId = currentModal.querySelector(`[id^="editTodoId"][id$="${todoId}"]`) || currentModal.querySelector('[id^="editTodoId"]');

    var viewImage = currentModal.querySelector(`[id^="viewImg"][id$="${todoId}"]`) || currentModal.querySelector('[id^="viewImg"]');

    if (editTodoTable) {
        editTodoTable.value = todoContent;
        log('Updated todo table content');
        console.log('Todo ID before submission:', todoId);  // 확인 로그 추가
        console.log('editTodoTable:', editTodoTable.value);
        console.log('todoText:', todoText);
        console.log('todoImage:', todoImage);

    } else {
        log('Edit todo table input not found');
    }

    if (editTodoText) {
        editTodoText.value = todoText;
        log('Updated todo text content');
    } else {
        log('Edit todo text input not found');
    }
    
    if (editTodoImage && todoImage) {
        editTodoImage.src = todoImage;
        editTodoImage.style.display = "block";
        log('Updated todo image');
    } else if (editTodoImage) {
        
        log('Todo image not found, hiding image element');
    } else {
        log('Edit todo image element not found');
    }
    if(editTodoId){
        editTodoId.value = todoId;
    }
    if(viewImage){
        viewImage.src = todoImage;
    }
}


// 모든 닫기 버튼에 이벤트 리스너 추가
document.querySelectorAll('.close').forEach(function(closeBtn) {
    closeBtn.onclick = closeCurrentModal;
});

// 모달 외부 클릭 시 닫기
window.onclick = function(event) {
    if (event.target == currentModal) {
        closeCurrentModal();
    }
};

function closeCurrentModal() {
    if (currentModal) {
        currentModal.style.display = "none";
        currentModal = null;
        log('Modal closed');
    }
}

// 초기화 로그
log('Modal script initialized');








    //별 버튼
    $('.btn-star').on('click', function(event) {
        event.preventDefault();  // 기본 form 제출 방지
    
        let button = $(this);
        let form = button.closest('form');
        let todoId = form.data('todo-id');  // form 태그의 data-todo-id 속성을 가져옴
        let csrfToken = form.find('input[name="csrfmiddlewaretoken"]').val();  // CSRF 토큰 가져오기
    
        // 콘솔로 값 출력해서 디버깅
        console.log("Todo ID: " + todoId);
        console.log("CSRF Token: " + csrfToken);
    
        $.ajax({
            url: './markAsStar/',  // 서버로 POST 요청 보낼 URL
            type: 'POST',
            data: {
                todo_id: todoId,
                csrfmiddlewaretoken: csrfToken  // CSRF 토큰 추가
            },
            success: function(response) {
                console.log('서버 응답 성공:', response);
    
                // 서버 응답이 성공적일 경우, 버튼의 색깔 및 텍스트를 변경
                if (button.text() === '☆') {
                    button.text('★');
                    button.css('color', 'orange');
                } else {
                    button.text('☆');
                    button.css('color', 'black');
                }
            },
            error: function(xhr, status, error) {
                console.error('별표 처리 실패:', error);
                console.error('응답 상태:', xhr.status);
            }
        });
    });





document.getElementById('todoImage').addEventListener('change', function(event) {
        var file = event.target.files[0];
        var reader = new FileReader();
    
        reader.onload = function(e) {
            var imagePreview = document.getElementById('imagePreview');
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block'; // 이미지 미리보기 보이도록 설정

            // 파일 입력 필드를 숨깁니다.
            event.target.style.display = 'none';
        };
    
        if (file) {
            reader.readAsDataURL(file);
        }
});


