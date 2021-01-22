from flask import Blueprint, request
import mysql.connector
from mysql.connector import Error
from models.user import User

room_blueprint = Blueprint('room_blueprint', __name__)

db = mysql.connector.connect(
	host="localhost",
	user="root",
	password="adminadmin"
)

name = 'gtemhack'
cursor = db.cursor()
cursor.execute("USE " + name)

@room_blueprint.route('/rooms')
def user_test():
    return 'Rooms Test'


@room_blueprint.route('/rooms/add-room', methods=['POST'])
def add_room():
    room_info = request.get_json()
    length = room_info['length']
    breadth = room_info['breadth']
    building = room_info['building']
    room = str(room_info['room'])
    room_id = building + "-" + room
    query = "INSERT INTO room (room_id, length, breadth) VALUES (%s, %s, %s)"
    values = (room_id, length, breadth)
    cursor = db.cursor()
    try:
        cursor.execute(query, values)
    except Error as err:
        print(err)
    finally:
        db.commit()
        cursor.close()
    

    cursor = db.cursor()
    query = "INSERT INTO config (room_id, seat_id, status, taken_by) VALUES (%s, %s, %s, %s)"
    for i in range(0, length):
        for j in range(0, breadth):
            values = (room_id, i * breadth + j, 'available', None)
            try:
                cursor.execute(query, values)
            except Error as err:
                print(err)
    db.commit()
    cursor.close()
    return 'Hello'


@room_blueprint.route('/rooms/get-current-configuration')
def get_current_config():
    cursor = db.cursor()
    info = request.get_json()

    room_id = info['room_id']

    query = "SELECT * FROM config WHERE room_id = '" + room_id + "'"

    return 'Hello'


@room_blueprint.route('/rooms/choose-seat', methods=['POST'])
def choose_seat():
    return 'Hello'

