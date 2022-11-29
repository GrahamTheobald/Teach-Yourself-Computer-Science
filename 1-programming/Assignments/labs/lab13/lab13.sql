.read data.sql

CREATE TABLE bluedog AS
  SELECT color, pet FROM students WHERE color = 'blue' AND pet = 'dog' ;

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song FROM students WHERE color = 'blue' AND pet = 'dog' ;

CREATE TABLE smallest_int_having AS
  SELECT time, min(smallest) FROM students GROUP BY smallest HAVING count(*) = 1;

CREATE TABLE matchmaker AS
  SELECT a.pet, a.song, a.color, b.color
  FROM students AS a, students AS b
  WHERE a.pet = b.pet AND a.song = b.song AND a.time < b.time;

CREATE TABLE sevens AS
  SELECT seven FROM students, numbers 
  WHERE students.time = numbers.time AND numbers.'7' = 'True' AND students.number = 7;

CREATE TABLE average_prices AS
  SELECT category, avg(MSRP) as average_price FROM products
  GROUP BY category;

CREATE TABLE lowest_prices AS
  SELECT store, item, min(price) FROM inventory
  GROUP BY item;

CREATE TABLE best_deal AS 
SELECT name, min(MSRP / rating) as deal FROM products GROUP BY category;

CREATE TABLE shopping_list AS
  SELECT best_deal.name, lowest_prices.store FROM best_deal, lowest_prices
  WHERE best_deal.name = lowest_prices.item;

CREATE TABLE total_bandwidth AS
  SELECT sum(stores.Mbs) FROM shopping_list, stores
  WHERE shopping_list.store = stores.store;