document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();  // 폼 제출을 막고
    console.log('폼 제출 시도됨');
});