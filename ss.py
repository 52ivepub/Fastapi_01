SELECT
    users.username,
    users.id,
    profiles_1.first_name,
    profiles_1.last_name,
    profiles_1.bio,
    profiles_1.user_id,
    profiles_1.id AS id_1
FROM
    users
    LEFT OUTER JOIN profiles AS profiles_1 ON users.id = profiles_1.user_id
ORDER BY
    users.id INFO sqlalchemy.engine.Engine


SELECT
    users.username,
    users.id,
    posts_1.title,
    posts_1.body,
    posts_1.user_id,
    posts_1.id AS id_1
FROM
    users
    LEFT OUTER JOIN posts AS posts_1 ON users.id = posts_1.user_id
ORDER BY
    users.id

    