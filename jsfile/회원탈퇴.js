var out = document.querySelector('#out');
out.addEventListener("click", okay);

function okay() {
    var userConfirmation = confirm("회원탈퇴시 재가입이 불가능 합니다 정말 탈퇴하시겠습니까?");
    if (userConfirmation) {
        alert("탈퇴가 완료되었습니다.");
    }
    }