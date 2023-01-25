# pincoin-dj
## 용도
* 도메인 모델 설계 및 마이그레이션 도구 활용
* 장고 관리자 활용
  * 시작 페이지 이외 text/html 응답 없음
* CLI 명령어 추가 배치(batch) 작업

## 의존성
* Django
  * django_
  * auth_
* mysqlclient

## 테이블 생성 패키지
* django-model-utils
* django-mptt
* django-taggit
  * taggit_
* django-otp
  * otp_
* django-allauth
  * account_
  * socialaccount_
* easy_thumbnails (이관 안함)
  * easy_thumbnails_

## 마이그레이션 대상 앱
우선순위
* member_
* shop_
차후 작업
* blog_
* book_
* board_ (미사용 이관 안 함)
* banner_ (미사용 이관 안 함)
* bookkeeping_ (미사용 이관 안 함)

# RDBMS
## MariaDB RDBMS
```
sudo mysql -uroot
> CREATE DATABASE pincoin CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
> CREATE USER 'pincoin'@'%' IDENTIFIED BY 'your_password'
> GRANT ALL PRIVILEGES ON pincoin.* TO 'pincoin'@'%';
> FLUSH PRIVILEGES;
```
