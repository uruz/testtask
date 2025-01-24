ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'rootpassword';

ALTER USER 'myuser'@'%' IDENTIFIED WITH mysql_native_password BY 'mypassword';

GRANT CREATE ON *.* TO 'myuser'@'%';
GRANT ALL PRIVILEGES ON `mydatabase`.* TO 'myuser'@'%';
GRANT ALL PRIVILEGES ON `test_mydatabase`.* TO 'myuser'@'%';

FLUSH PRIVILEGES;
