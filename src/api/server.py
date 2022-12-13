'''Server for the OSP API'''
from flask import Flask, request
import json
import psycopg2
import src.api.constants as server_constants

app = Flask(__name__)

if server_constants.RUN_SERVER:
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='postgres',
            database='osp_database'
        )
    except psycopg2.Error as err:
        print(f'Error connecting to database: {err}')

    cursor = connection.cursor()

def create_database():
    connection.set_isolation_level(
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cursor.execute('CREATE DATABASE osp_database')

    cursor.close()
    cursor.close()


@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/getusers')
def get_users():
    res = json.dumps(get_members())
    return res

def get_members():
    """Select all members from members table"""
    try:
        sql = 'SELECT * FROM members'
        cursor.execute(sql)
    except (connection.error, sql.ProgrammingError, sql.connection) as e:
        print(f'error writing to database: {e}')
    finally:
        connection.commit()
    return cursor.fetchall()

@app.route('/greet', methods=['POST'])
def greet():
    print(request)
    name = request.form['name']
    return f'Hello, {name}!'

def start():
    app.run()
