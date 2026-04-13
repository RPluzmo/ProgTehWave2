USE wave_friend2;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(10) NOT NULL,
email VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
birthdate DATE NOT NULL,
gender ENUM('woman', 'man', 'nonbinary', 'other') NOT NULL,
bio TEXT NOT NULL
);
