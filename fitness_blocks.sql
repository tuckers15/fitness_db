--@block opening fitness
USE fitness;
--@block creating workout table
CREATE TABLE workouts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
--@block creating users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    discord_id BIGINT,
    discord_user VARCHAR(20)
);
--@block creating workouts_exercises
CREATE TABLE workouts_exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    workout_id INT,
    exercise_id INT,
    weight_load INT,
    reps INT,
    set_count INT
);
--@block creating exercises table
CREATE TABLE exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20)
);
--@block
SELECT *
FROM workouts;
--@block creating a new workout
INSERT INTO workouts (user_id, start_time)
VALUES(2, NOW());
--@block stopping above workout
UPDATE workouts
SET end_time = NOW()
WHERE id = 6;
--@block
DESCRIBE workouts_exercises;
--@block
SELECT *
FROM workouts_exercises;
--@block
CREATE TABLE workouts_exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    workout_id INT,
    exercise_id INT,
    weight_load FLOAT,
    reps INT,
    set_count INT,
    FOREIGN KEY (workout_id) REFERENCES workouts(id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
);