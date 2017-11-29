# FastCampus - Project
 
## 반려동물 : 관리/의료서비스 

- 반려동물 프로필 기록, 생의 주기
- 병원 위치 , 예방접종 날짜 알림, 신체정보, 질병 및 수술
- 커뮤니티 기능

### WPS 멤버 : 김진석, 장근희, 승형수

---

### 17/11/22 v0.1

- 기본 User 모델 및 API View 구현
- Elasticbeanstalk 배포 준비를 위한 Dockerfile 생성 및 테스트 완료

### 17/11/22 v0.1.4

- Elasticbeanstalk 배포에 따른 각종 오류 해결
 - `.config_secret` 폴더 업로드를 위한 `.ebignore` 파일 작성
 - Django의 Allowed_Host 옵션 추가
 - ELB Healthcheck에 대비하기 위한 코드 추가

### 17/11/23 v0.2.1

- 이메일 회원가입 인증 프로세스 추가
 - celery & rabbitMQ를 이용한 비동기 태스크 구현
 
### 17/11/29 v0.3

- travis CI 적용
 - 테스트 코드 작성
- User API 뷰 작성
- Pet 모델링
 - 동물 사람 나이 환산 함수 구현
- 기존 계정 해킹에 따른 재 배포
 - wooltari.co.kr에 도메인 연결
 - http를 https로 리다이렉트하는 ebextensions 파일 추가
 
