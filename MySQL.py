import pymysql
import mysql.connector
db=mysql.connector.connect( database =  "Local instance MySQL80" ,
        USER="root",
        HOST= "127.0.0.1",
        passwd="123456",
        PORT= "3306" )