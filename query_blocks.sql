-- SQL Blocks to be turned into commands --;
--@block Get exercises from a wokrout
SELECT *
FROM workouts_exercises
WHERE workout_id = 2;
--@block Get wrokouts by user
SELECT *
FROM workouts
WHERE user_id = 1;