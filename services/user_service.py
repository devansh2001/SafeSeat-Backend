from flask import Blueprint, request
import mysql.connector
from mysql.connector import Error
from models.user import User

user_blueprint = Blueprint('user_blueprint', __name__)

db = mysql.connector.connect(
	host="localhost",
	user="root",
	password="adminadmin"
)

name = 'gtemhack'
cursor = db.cursor()
cursor.execute("USE " + name)

@user_blueprint.route('/user')
def user_test():
    return 'User Test'

@user_blueprint.route('/user/add', methods=['POST'])
def add_user():
    cursor = db.cursor()
    user_info = request.get_json()
    print('USER: Received to add ')
    print(user_info)
    query = "INSERT INTO user (name, email, password, role) VALUES (%s, %s, %s, %s)"
    values = (user_info['name'], user_info['email'], user_info['password'], user_info['role'])
    try:
        cursor.execute(query, values)
    except Error as err:
        print(err)
    finally:
        db.commit()
        cursor.close()
    return {'response': 'OK'}


@user_blueprint.route('/user/retrieve/<email>')
def get_user(email):
    query = "SELECT * FROM user WHERE email = '" +  email + "'"
    print("USER: Executing - " + query)

    cursor = db.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result is None:
            return 'No user found!'
        user_result = result[0]
        user = {
            'name': user_result[0],
            'email': user_result[1],
            'password': user_result[2],
            'role': user_result[3],
            'classes': get_classes(user_result[1])
        }
        return user
    except Error as err:
        print(err)
    finally:
        cursor.close()
    # user = User()
    return 'Error'

@user_blueprint.route('/user/change-classes', methods=['POST'])
def modify_classes():
    cursor = db.cursor()
    info = request.get_json()

    email = info['email']
    classes = info['classes']

    query = "DELETE FROM takes where email = '" + email + "'"
    try:
        cursor.execute(query)
    except Error as e:
        print(e)
    finally:
        db.commit()
        cursor.close()

    cursor = db.cursor()
    query = "INSERT INTO takes (email, class) VALUES (%s, %s)"
    try:
        for i in range(0, len(classes)):
            values = (email, classes[i])
            cursor.execute(query, values)
    except Error as e:
        print(e)
    finally:
        db.commit()
        cursor.close()

    return {'response': 'OK'}


def get_classes(email):
    cursor = db.cursor()

    query = "SELECT class FROM takes WHERE email = '" + email + "'"
    print("Executing: " + query)
    classes = []
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for i in range(0, len(result)):
            classes.append(result[i])
    except Error as err:
        print(err)
    finally:
        cursor.close()
    
    
    return classes
