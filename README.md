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
CREATE TABLE public.lunch_menu (
	id serial NOT NULL,
	menu_name text NOT NULL,
	member_name text NOT NULL,
	dt date NOT NULL,
	CONSTRAINT lunch_menu_pk PRIMARY KEY (id)
);

alter table lunch_menu
add constraint unique_member_dt unique (member_name, dt);

insert into member(name)
values
('TOM'),
('cho'),
('hyun'),
('JERRY'),
('SEO'),
('jiwon'),
('jacob'),
('heejin'),
('lucas'),
('nuni');

select jsonb_object_agg(name,id)
from(
	select name , id from member order by id
)temp;
{"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}


alter table lunch_menu
add column member_id int;

select * from lunch_menu limit 1;


-- 사용하지 않는 컬럼 삭제
alter table lunch_menu
drop column member_name;

-- member_id null 값을 허용하지 않도록 설정
-- delete from lunch_menu;
alter table lunch_menu
alter column member_id set not null;

-- 새로운 제약 조건 추가
alter table lunch_menu 
add constraint unique_member_id_dt unique (member_id,dt);

-- rename
ALTER TABLE public.lunch_menu RENAME CONSTRAINT unique_memberid_dt TO unique_member_id_dt;


-- 멤버 테이블 
alter table member
add constraint member_id_pk primary key(id);

-- 관계 조건 추가
alter table lunch_menu 
add constraint menu_member_fk
	foreign key (member_id)
	references member(id)
;

--테스트
select * from member;

select max(id) from member; -- 10

select * from lunch_menu;

insert into lunch_menu(menu_name, member_id, dt)
values('햄버거', 3,'2025-01-01')

insert into lunch_menu(menu_name, member_id, dt)
values('햄버거', 11,'2025-01-01')
-- SQL Error [23503]: ERROR: insert or update on table "lunch_menu" violates foreign key constraint "menu_member_fk" Detail: Key (member_id)=(11) is not present in table "member".


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
