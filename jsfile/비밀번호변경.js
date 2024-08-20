function changePassword(currentPwd, newPwd) {
    // CSRF 토큰을 메타 태그에서 가져오기 (이미 HTML에 포함되어 있어야 함)
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('/api/users/pwd', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token'), // Authorization 헤더에 토큰 포함
            'X-CSRFToken': csrfToken // CSRF 토큰 포함
        },
        body: JSON.stringify({
            currentPwd: currentPwd, // 현재 비밀번호
            newPwd: newPwd          // 새 비밀번호
        })
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 400) {
                throw new Error("잘못된 요청입니다. 입력한 데이터를 확인하세요.");
            } else if (response.status === 401) {
                throw new Error("인증되지 않은 사용자입니다. 다시 로그인 해주세요.");
            } else if (response.status === 403) {
                throw new Error("현재 비밀번호가 일치하지 않습니다.");
            } else {
                throw new Error("서버 오류가 발생했습니다. 잠시 후 다시 시도하세요.");
            }
        }
        return response.json();
    })
    .then(data => {
        alert(data.message); // 서버의 응답 메시지 출력
    })
    .catch(error => {
        alert(error.message); // 에러 메시지 출력
    });
}

// 비밀번호 변경 버튼 클릭 이벤트에 함수 연결
document.querySelector("#changePasswordBtn").addEventListener("click", function() {
    const currentPwd = document.querySelector("#currentPwd").value;
    const newPwd = document.querySelector("#newPwd").value;

    // 비밀번호 변경 함수 호출
    changePassword(currentPwd, newPwd);
});