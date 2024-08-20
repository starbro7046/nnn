document.getElementById('loginbtn').addEventListener('click', function(event) {
    event.preventDefault(); // 폼의 기본 제출 동작을 막음

    const username = document.getElementById('user-id').value;
    const password = document.getElementById('password').value;

    fetch('/api/users/login', {     
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('서버 응답이 올바르지 않습니다.');
        }
        return response.json();
    })
    .then(data => {
        if (data.message === "로그인 성공") {
            alert('로그인 성공!');
            // 로그인 성공 시의 처리 (예: 페이지 이동)
            window.location.href = '../home';
        } else {
            alert('로그인 실패: ');
        }
    })
    .catch(error => {
        if (error.message.includes('401')) {
            alert('로그인 실패: 아이디 또는 비밀번호가 잘못되었습니다.');
        } else if (error.message.includes('400')) {
            alert('로그인 실패: 잘못된 요청입니다.');
        } else {
            alert('로그인 중 오류가 발생했습니다.');
        }
    });
});