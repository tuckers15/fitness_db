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
--@block updating workouts to use foreign id and cascade/restriction
ALTER TABLE workouts
ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE RESTRICT;
--@block for show_workout()
SELECT discord_user as 'Name',
    DATE_FORMAT(workouts.date, '%m-%d-%y') as 'Date',
    GROUP_CONCAT(exercises.name SEPARATOR ', ') as 'Exercises'
FROM workouts
    JOIN users ON users.id = workouts.user_id
    JOIN workouts_exercises on workouts.id = workouts_exercises.workout_id
    JOIN exercises on workouts_exercises.exercise_id = exercises.id
WHERE workouts.id = 8
GROUP BY workouts.id,
    users.discord_user,
    workouts.date
ORDER BY workouts.date DESC;