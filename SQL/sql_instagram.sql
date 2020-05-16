CREATE TABLE usernames_queue_1 (username TEXT UNIQUE NOT NULL);
CREATE TABLE usernames_visited_1 (username TEXT UNIQUE NOT NULL);

SELECT * FROM usernames_queue_1;
SELECT * FROM usernames_visited_1;

CREATE TABLE data_1 (
	username TEXT NOT NULL, 
	follower_count TEXT NOT NULL,
	following_count TEXT NOT NULL, 
	media_count TEXT NOT NULL,
	name TEXT NOT NULL, 
	biography TEXT NOT NULL,
	followers TEXT NOT NULL, 
	followings TEXT NOT NULL,
	isPrivate TEXT NOT NULL
);

select * from data_1;

SELECT COUNT(*) FROM data_1;

SELECT COUNT(*) FROM data_1 WHERE followers = 'NULL';

SELECT COUNT(*) FROM data_1 WHERE followers != 'NULL';

SELECT COUNT(*) FROM usernames_queue_1;

SELECT COUNT(*) FROM usernames_visited_1;
