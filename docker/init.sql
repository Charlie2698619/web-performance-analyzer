-- Set authentication plugin for the user
ALTER USER 'devcharlie'@'%' IDENTIFIED WITH mysql_native_password BY 'devcharlie';
ALTER USER 'devcharlie'@'localhost' IDENTIFIED WITH mysql_native_password BY 'devcharlie';
FLUSH PRIVILEGES;
