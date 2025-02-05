# lunch-menu
- [] 나의 점심메뉴를 수집
- [] 분석
- [] 알람 (오늘 입력하지 않았으면 입력 혹은 로컬이 아닌 사람들에게 제공한다면 입력하지 않은 사람들에게 제공)
- [] *CSV to DB* 집중!
- [] 
# Ready For me

## Install DB with Docker
- https://hub.docker.com/_/postgres
``` bash
$ sudo docker run --name local-postgres \
-e POSTGRES_USER=sunsin \
-e POSTGRES_USER=mysecretpassword \
-e POSTGRES_DB=sunsindb \
-p 5432:5432\
-d postgres:15.10
```
## Create Table
- postgres

```sql
CREATE TABLE public.lunch_menu(
        id serial NOT NULL,
        menu_name text NOT NULL,
        member_name text NOT NULL,
        dt date NOT NULL,
        COMSTRAINT lunch_menu_pk PRIMARY KEY (id)
```

## Dev
```bash
# DB Check, Start, Stop, Remove
$ history | grep docker | grep run
$ sudo docker stop local-postgres
$ sudo docker start local-postgres
$ sudo docker stop local-postgres
$ sudo docker rm local-postgres

# Into CONTAINER
# sudo docker exec -it local-postgres bash
```

- RUN
```bash
# DB 정보에 맞춰 수정 
$ cp env.dummy .env\
# 서버 시작
$ streamlit run App.py
