# database
https://www.jdoodle.com/execute-sql-online/

'''---
61.Product資料表包含下列資料。
ID NAME Quantity
1234 Spoon 33
2615 Fork 17
3781 Plate 20
4589 Cup 51
您執行下列陳述式:
SELECT COUNT(*)
  FROM Product WHERE Quantity > 18
此陳述式會傳回的值是什麼?
A. 1
B. 2
C. 3
D. 4
==
create table product(id text, name text, quantity int);
insert into product values("1234","Spoon",33);
insert into product values("2615","Fork",17);
insert into product values("3781","Plate",20);
insert into product values("4589","Cup",51);
select * from product;
SELECT COUNT(*)
  FROM Product WHERE Quantity > 18
==
'''
