import csv
import pandas
import mysql.connector

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

TABLES['movieData'] = ("""
    CREATE TABLE `movieData` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `rating` int(11) NOT NULL,
        `title` varchar(255) NOT NULL,
        `year` int(4) NOT NULL,
        `director` varchar(255) NOT NULL,
        `genre` varchar(255) NOT NULL,
        PRIMARY KEY ('id')
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

cnx.close()