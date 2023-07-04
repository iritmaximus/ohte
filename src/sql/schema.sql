CREATE TABLE IF NOT EXISTS Users (
    id serial primary key not null,
    name varchar(255) not null unique,
    password_hash varchar(255) not null,
    rating integer CONSTRAINT positive_rating CHECK (rating > 0)
);

CREATE TABLE IF NOT EXISTS Games (
    id serial primary key not null,
    result varchar(10),
    white_id integer not null,
    black_id integer not null,
    rated boolean default true,
    foreign key (white_id)
        references Users (id)
            on delete set null,
    foreign key (black_id)
        references Users (id)
            on delete set null
);
