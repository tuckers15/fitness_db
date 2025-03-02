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
    discord_id INT
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
INSERT INTO workouts (user_id)
VALUES()