function toggleBox(button, boxClass, textColor) {
    // 클릭된 버튼의 부모 요소인 timebox 또는 timebox2를 찾습니다.
    var ckDiv = button.closest(boxClass);

    // hidden-content 요소를 찾습니다.
    var hiddenContent = ckDiv.querySelector('.hidden-content');

    // list-label 요소를 찾습니다.
    var listLabel = ckDiv.querySelector('.list-label');

    // 현재 hiddenContent의 computed style을 가져옵니다.
    var currentDisplay = window.getComputedStyle(hiddenContent).display;

    // hidden-content의 표시 상태를 토글합니다.
    if (currentDisplay === 'none') {
        hiddenContent.style.display = 'block';
        hiddenContent.style.color = textColor; // 전달된 색상으로 설정
        hiddenContent.style.fontWeight = 'lighter'; // 폰트의 굵기를 얇게 설정
        var hiddenContentHeight = hiddenContent.offsetHeight; // hidden-content의 높이를 가져옴
        ckDiv.style.height = hiddenContentHeight + 20 + 'px';  // hiddenContent 높이 + 30px

        // list-label의 margin-top을 조정합니다.
        listLabel.style.marginTop = '35px'; // 원하는 값으로 설정
    } else {
        hiddenContent.style.display = 'none';
        ckDiv.style.height = '';  // 원래 height 값을 복원합니다.

        // list-label의 margin-top을 원래대로 복원합니다.
        listLabel.style.marginTop = '0'; // 기본 값으로 복원
    }
}

function toggleMemoBox(button) {
    toggleBox(button, ".timebox", "black");  // 글씨 색상을 검은색으로 설정
}

function toggleDoneBox(button) {
    toggleBox(button, ".timebox2", "white");  // 글씨 색상을 흰색으로 설정
}



  // 현재 날짜와 시간을 가져오기
  function displayCurrentDateTime() {
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    const formattedDateTime = `${year}-${month}-${day}`;
    document.getElementById("currentDateTime").textContent = ` ${formattedDateTime}`;
}

// 함수 호출하여 날짜와 시간 표시
displayCurrentDateTime();


//12월 달력 임시

function createCalendar() {
    const calendarBody = document.getElementById('calendarBody');
    const daysInDecember = 31;
    const startDay = 0; // 12월 1일은 일요일

    // 첫 주 빈칸 채우기
    for (let i = 0; i < startDay; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.classList.add('day', 'empty');
        calendarBody.appendChild(emptyCell);
    }

    // 날짜 채우기
    for (let day = 1; day <= daysInDecember; day++) {
        const dayCell = document.createElement('div');
        dayCell.classList.add('day');
        dayCell.textContent = day;
        calendarBody.appendChild(dayCell);
    }
}

// 함수 호출하여 달력 생성
createCalendar();