# pincoin-dj
## 목적
* 도메인 모델 설계 및 마이그레이션 도구 활용
* 장고 관리자 활용
  * 시작 페이지 이외 text/html 응답 없음
* CLI 명령어 추가 배치(batch) 작업

## 의존성
### 장고 기본 패키지
* Django
  * django_
  * auth_
* mysqlclient

### 주요 테이블 생성 패키지
* django-model-utils
* django-mptt
* django-otp
  * otp_
* django-allauth
  * account_
  * socialaccount_
* django-taggit
  * taggit_
* easy-thumbnails
  * easy_thumbnails_

### 주요 이관 앱
* member_
* shop_
* blog_
* book_
* board_ (미사용/이관 안 함)
* banner_ (미사용/이관 안 함)
* bookkeeping_ (미사용/이관 안 함)

# 주요 설정
## MariaDB RDBMS
```
sudo mysql -uroot
> CREATE DATABASE pincoin CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
> CREATE USER 'pincoin'@'%' IDENTIFIED BY 'your_password'
> GRANT ALL PRIVILEGES ON pincoin.* TO 'pincoin'@'%';
> FLUSH PRIVILEGES;
```

## 다국어
```
python manage.py makemessages -l ko -i venv
```

```
python manage.py makemessages -a -i venv
python manage.py compilemessages -i venv
```