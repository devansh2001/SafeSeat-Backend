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
            seat_id = i * breadth + j
            seat_availability = 'available' if seat_id % 2 == 0 else 'full'
            values = (room_id, seat_id, seat_availability, None)
            try:
                cursor.execute(query, values)
            except Error as err:
                print(err)
    db.commit()
    cursor.close()
    return 'Hello'


@room_blueprint.route('/rooms/get-current-configuration/<room_id>')
def get_current_config(room_id):
    cursor = db.cursor()
    # info = request.get_json()
    # room_id = info['room_id']

    query = "SELECT length, breadth from room where room_id = '" + room_id + "'"
    length = 0
    breadth = 0
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        result = result[0]
        length = result[0]
        breadth = result[1]
    except Error as err:
        print(err)
    finally:
        cursor.close()
    
    print(length, breadth)

    cursor = db.cursor()

    query = "SELECT * FROM config WHERE room_id = '" + room_id + "'"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        seats = []
        for i in range(0, length):
            curr_row = []
            for j in range(0, breadth):
                curr_seat = result[i * breadth + j]
                curr_seat_info = {
                    'id': curr_seat[1],
                    'isReserved': True if curr_seat[2] == 'full' else False,
                    'number': curr_seat[1]
                }
                curr_row.append(curr_seat_info)
            seats.append(curr_row)
        return {'seats' : seats}
    except Error as err:
        print(err)
    finally:
        cursor.close()
    return {'response': 'ERROR'}


@room_blueprint.route('/rooms/choose-seat', methods=['POST'])
def choose_seat():
    info = request.get_json()
    room_id = info['room_id']
    seat_id = str(info['seat_id'])
    email = info['email']
    cursor = db.cursor()
    query = "UPDATE config SET status = 'full', taken_by = '" + email + "' where room_id = '" + room_id + "' and seat_id = " + seat_id

    try:
        cursor.execute(query)
    except Error as err:
        print(err)
    finally:
        db.commit()
        cursor.close()

    return {'response': 'OK'}

