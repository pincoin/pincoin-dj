# pincoin-dj
## 용도
* 도메인 모델 설계 및 마이그레이션 도구 활용
* 장고 관리자 활용
  * 시작 페이지 이외 text/html 응답 없음
* CLI 명령어 추가 배치(batch) 작업

## 의존성
* Django
* mysqlclient
* django-otp

## 마이그레이션 대상 앱
우선순위
* member
* shop
차후 작업
* banner
* blog
* board
* book

# RDBMS
## MariaDB RDBMS
```
sudo mysql -uroot
> CREATE DATABASE pincoin CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
> CREATE USER 'pincoin'@'%' IDENTIFIED BY 'your_password'
> GRANT ALL PRIVILEGES ON pincoin.* TO 'pincoin'@'%';
> FLUSH PRIVILEGES;
```
