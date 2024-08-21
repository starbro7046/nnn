document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('fetchDataBtn').addEventListener('click', function() {
        const url = 'https://flaunchtest-mczuu.run.goorm.site/login/';

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

    const bookmarkIcon = document.getElementById('bookmark-icon');
    const likeIcon = document.getElementById('like-icon');

    bookmarkIcon.addEventListener('click', () => {
        bookmarkIcon.classList.toggle('bookmarked');
    });

    likeIcon.addEventListener('click', () => {
        likeIcon.classList.toggle('fas');
        likeIcon.classList.toggle('far');
        likeIcon.classList.toggle('liked');
    });

    // CSRF 토큰 설정
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Axios를 이용한 챌린지 데이터 가져오기
    async function fetchUserChallenges(board) {  const url = 'https://jsonplaceholder.typicode.com/posts';
        const token = 'your_token_here'; // 여기에 실제 토큰 값을 넣어주세요.

        try {
            const response = await axios.get(`https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth`, {
                headers: {
                    'authorization': token,
                    'X-CSRF-TOKEN': csrfToken // CSRF 토큰 추가
                }
            });
            if (response.status === 200) {
                console.log('챌린지 정보:', response.data);
            }
        } catch (error) {
            if (error.response) {
                if (error.response.status === 401) {
                    console.error('인증 오류: 토큰이 유효하지 않거나 만료되었습니다.');
                } else if (error.response.status === 500) {
                    console.error('서버 오류: 서버에서 문제가 발생했습니다.');
                } else {
                    console.error(`오류 발생: ${error.response.status} - ${error.response.data}`);
                }
            } else {
                console.error('네트워크 오류 또는 요청이 서버에 도달하지 못했습니다.');
            }
        }
    }

});