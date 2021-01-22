from flask import Blueprint, request
import mysql.connector
from mysql.connector import Error
from models.user import User

room_blueprint = Blueprint('rooms_blueprint', __name__)

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
    return 'Hello'


@room_blueprint.route('/rooms/get-current-configuration')
def add_room():
    return 'Hello'


@room_blueprint.route('/rooms/choose-seat', methods=['POST'])
def add_room():
    return 'Hello'

