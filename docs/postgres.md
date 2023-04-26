# Postgres database

## Note for the advanced
The documentation for these steps can also be found in [Arch wiki](https://wiki.archlinux.org/title/PostgreSQL),
but for the sake of this course, I will also write "quick-start" quide here.

## About sudo
If you have `sudo` rights on the school computer, use [this](https://wiki.helsinki.fi/display/it4sci/Administrator+%28sudo%29+rights+in+Cubbli+Linux).


## Installing Postgres
Install `postgres` on your machine.

On school laptops running the command should install `postgres`
```bash
sudo apt install postgresql
```

If not, follow the links below.
* [Postgres install, official site](https://www.postgresql.org/download/)
* [Postgres install, Ubuntu/Cubbli](https://ubuntu.com/server/docs/databases-postgresql)

## Configuration
After installing `postgres` we must first configure it to ensure things work the way we want.

### Switching to "postgres" user
We need to switch to the `postgres` user on our system
so we have the permissions to create our own.

Use `sudo` to switch to postgres user.
```bash
$ sudo -iu postgres
```

### Database cluster initialization
As the `postgres` user run this to initialize the database cluster to the
path.
```bash
[postgres]$ initdb -D /var/lib/postgres/data
```

If the initialization was successful, start `postgres` as a system service.
```bash
$ sudo systemctl enable postgresql.service
$ sudo systemctl start postgresql.service
```

### Psql
After running `postgres` as a system service, you can access `postgres` shell with the `psql` command.
```bash
[postgres]$ psql
```
or
```bash
$ psql -U postgres
```
if you are not logged in as the postgres user where `postgres` is the user's name you wish to login in as.

### Creating user/database
As the postgres user, run
```bash
[postgres]$ createuser --interactive
```

Then create the two databases with the username you created in the previous step.
As you need to create TWO databases, you could, for example, add "test_" prefix to the test-database name.
```bash
[postgres]$ createdb myDatabaseName -O your_username
```

#### Note
If you create postgres user with the same name as your linux user,
it allows you to access `psql` without having to specify the user to login.
You can also omit the `-O` flag from the `createdb` command.

### Final steps
If you managed to create user and two databases, you have what you need.
There are many optional security steps to take but as I would need to write all this by myself,
here is a link to a [wiki page](https://wiki.archlinux.org/title/PostgreSQL#Optional_configuration).
