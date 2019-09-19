CREATE TABLE user(
  id integer primary key AUTOINCREMENT,
  name text,
  rating real,
  nationality text
);

CREATE TABLE request(
  id integer primary key,
  user_id integer,
  category integer,
  latitude real,
  longitude real,
  message text,
  helper_id integer,
  status integer default 0
  /* 0: 助け人探し 1: 合流中 2:助けられ中 3: 完了済み*/
);

insert into user(name, rating, nationality) values('情熱 猿人', 0, 'Japan');
insert into user(name, rating, nationality) values('浅井 太郎', 0, 'Japan');
insert into user(name, rating, nationality) values('筑波 太郎', 0, 'Japan');
insert into user(name, rating, nationality) values('水戸 次郎', 0, 'Japan');
insert into user(name, rating, nationality) values('土浦 三郎', 0, 'Japan');
insert into user(name, rating, nationality) values('John Smith', 0, 'U.S.A');
insert into user(name, rating, nationality) values('Michael jackson', 0, 'U.S.A');
insert into user(name, rating, nationality) values('Leonardo Wilhelm DiCaprio', 0, 'U.S.A');
insert into user(name, rating, nationality) values('Martin Luther King, Jr.', 0, 'U.S.A');
insert into user(name, rating, nationality) values('L.L. Zamenhof', 0, 'Porland');
insert into request (user_id, latitude, longitude, message) values(8, 0, 0, 'Please, take me to Tokyo station. And let''s dance with me!');
insert into request (user_id, latitude, longitude, message) values(9, 0, 0, 'I have a dream.');
insert into request (user_id, latitude, longitude, message) values(10, 0, 0, 'Kie estas la Tokio statio?');
