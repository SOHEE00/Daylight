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