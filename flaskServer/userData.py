import csv
import pandas
import mysql.connector

def insert_user(username, password, email, cnx, cursor):
    add_user = ("INSERT INTO users "
                "(username, password, email) "
                "VALUES (%s, %s, %s)")
    data_user = (username, password, email)
    cnx.cursor.execute(add_user, data_user)
    cnx.commit()
    return cnx.cursor.lastrowid

def authenticate_user(username, password, cnx, cursor):
    query = ("SELECT id FROM users WHERE username = %s AND password = %s")
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result

def insert_movie(date, title, year, rating, user, cnx, cursor):
    add_movie = ("INSERT INTO movieRatings "
                    "(date, title, year, rating, userId) "
                    "VALUES (%s, %s, %s, %s, %s)")
    data_movie = (date, title, year, rating, user)
    cursor.execute(add_movie, data_movie)
    cnx.commit()
    return cursor.lastrowid

def insert_csv(file_path, user):
    df = pandas.read_csv(file_path)
    try:
        for index, row in df.iterrows():
            insert_movie(row['Date'], row['Name'], row['Year'], row['Rating'], user)
    except Exception as e:
        print(f"Invalid File Format: {e}")

def init_db():
    cnx = mysql.connector.connect(user='root', password='password',
                                host='127.0.0.1 ',
                                database='movies')

    cursor = cnx.cursor()
    TABLES = {}

    TABLES['users'] = ("""
        CREATE TABLE `users` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `username` varchar(50) NOT NULL,
            `password` varchar(50) NOT NULL,
            `email` varchar(100) NOT NULL,
            `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB """)

    TABLES['movieRatings'] = ("""
        CREATE TABLE `movieRatings` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `rating` int(11) NOT NULL,
            `title` varchar(255) NOT NULL,
            `date` varchar(10) NOT NULL,
            `year` int(4) NOT NULL,
            `userId` int(11) NOT NULL,
            FOREIGN KEY (`userId`) REFERENCES `users`(`id`),
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB """)


    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    return cnx, cursor

def drop_db(cnx, cursor):
    cursor.execute(f"DROP TABLE movieRatings")
    cursor.execute(f"DROP TABLE users")
    cnx.close()

