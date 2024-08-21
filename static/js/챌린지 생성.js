document.getElementById('join-challenge-button').addEventListener('click', async () => {"https://jsonplaceholder.typicode.com/posts"
document.getElementById('fetchDataBtn').addEventListener('click', function() {
        const url = 'https://jsonplaceholder.typicode.com/posts';

        fetch(url)
            .then(response => response.json())
            .then(data => {
                document.getElementById('dataDisplay').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                document.getElementById('dataDisplay').textContent = 'An error occurred while fetching data.';
            });
    });




    const token = 'your_token_here'; // 실제 토큰 값으로 교체하세요.
    const board = 'your_board_id'; // 실제 board 값으로 교체하세요.
    const postId = 'your_post_id'; // 실제 postId 값으로 교체하세요.

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // CSRF 토큰 가져오기

    const requestBody = {
        challengeId: 'unique_challenge_id', // 실제 챌린지 ID로 교체하세요.
        username: 'your_username' // 실제 사용자 이름으로 교체하세요.
    };

    try {
        const response = await axios.post(`/api/challenges/${board}/${postId}`, requestBody, {
            headers: {
                'authorization': token,
                'Content-Type': 'application/json', // 요청 헤더에 JSON 형식 명시
                'X-CSRF-TOKEN': csrfToken // CSRF 토큰 추가
            }
        });

        if (response.status === 200) {
            console.log('챌린지 참가 성공:', response.data);
            // 성공 시 수행할 작업 추가 (예: 참가 완료 메시지 표시)
        }
    } catch (error) {
        if (error.response) {
            // 서버에서 오류 응답을 반환한 경우
            if (error.response.status === 400) {
                console.error('잘못된 요청: 요청 데이터를 확인하세요.');
            } else if (error.response.status === 404) {
                console.error('찾을 수 없음: 챌린지 또는 게시물을 찾을 수 없습니다.');
            } else if (error.response.status === 500) {
                console.error('서버 오류: 서버에서 문제가 발생했습니다.');
            } else {
                console.error(`오류 발생: ${error.response.status} - ${error.response.data}`);
            }
        } else {
            // 요청이 서버에 도달하지 못한 경우
            console.error('네트워크 오류 또는 요청이 서버에 도달하지 못했습니다.');
        }
    }
});