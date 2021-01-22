from flask import Blueprint

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/user')
def user_test():
    return 'User Test'
