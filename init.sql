-- Изменяем аутентификацию для root пользователя
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'rootpassword';

-- Изменяем аутентификацию для нашего пользователя
ALTER USER 'myuser'@'%' IDENTIFIED WITH mysql_native_password BY 'mypassword';

-- Применяем изменения
FLUSH PRIVILEGES;