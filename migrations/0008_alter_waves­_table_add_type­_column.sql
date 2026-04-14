USE wave_friend2;

ALTER TABLE waves
ADD type ENUM('regular', 'super') NOT NULL DEFAULT 'regular';