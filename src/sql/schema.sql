CREATE TABLE IF NOT EXISTS Users (
    id integer primary key autoincrement not null,
    name varchar(255) not null,
    rating integer
)

CREATE TABLE IF NOT EXISTS Games (
    id integer primary key autoincrement not null,
    result varchar(10),
    user_id integer not null,
    foreign key (user_id)
        references Users (id)
)
