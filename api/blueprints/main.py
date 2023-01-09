import json, uuid, datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)
# always import models below blueprint object creation
from ..models.user_model import User


@main.route('/')
def index():
    return "Hola! Welcome to Model.ai backend API!"


# '/register', post
@main.route('/register', methods=['POST'])
def register_post():
    # get payload data
    payload_data = json.loads(request.data)
    # users data
    id = str(uuid.uuid1())
    email = payload_data.get('email')
    password = payload_data.get('password')
    hashed_password = generate_password_hash(password, method='sha256')
    create_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  
    try:
        # if any required fields are missing
        if (email == None or password == None):
            resp = jsonify({'message': 'Missing user information'})
            resp.status_code = 302
            return resp

        user = User.get_user_by_email(email=email)
        # if user with passed email id  already exist
        if (user):
            resp = jsonify(
                {'message': f'User already exit with the mail-id: { email }'})
            resp.status_code = 201
            return resp
        else:
            # crate new user object
            new_user = User(id=id,
                            email=email,
                            password=hashed_password,
                            create_datetime=create_datetime,
                            update_datetime=update_datetime)
            # write data in database
            User.create_user(new_user)
            
            resp = jsonify({
                'message': f'User {email} created successfully',
                'data': []
            })
            resp.status_code = 201
            return resp
    except Exception as e:
        resp = {'message': 'Something went wrong!', 'error': str(e)}
        # resp.status_code = 500
        return resp


# '/login', post
@main.route('/login', methods=['POST'])
def login_post():
    # get payload data
    payload_data = json.loads(request.data)
    # get data from request payload
    email = payload_data.get('email')
    password = payload_data.get('password')

    # check if any required fields are missing
    if (email == None or password == None):
        resp = jsonify({'message': 'Missing login information'})
        resp.status_code = 302
        return resp

    #  find user against email
    user = User.get_user_by_email(email=email)

    # if user with email doesnt exist or password doesnt match
    if not user or not check_password_hash(user.password, password):
        resp = jsonify({'message': 'Incorrect username or password.'})
        resp.status_code = 403
        return resp

    # TODO: check if email is verified
    resp = jsonify({'message': 'Signin Successful.', 'access_token': user.id})
    # resp = jsonify({'message': 'Signin Successful.',
    #                'data': user.object_to_json()})
    resp.status_code = 201

    return resp


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``
# profile_post
@main.route('/profile', methods=['POST'])
def profile_post():
    # get payload data
    payload_data = json.loads(request.data)
    access_token = payload_data.get('access_token')


    # check if access_token is present
    if (not access_token):
        resp = jsonify({'message': 'Access Token Cannot be empty.'})
        # resp.message = 'Access Token Cannot be empty.'
        resp.status_code = 401  # HttpResponse
    elif (access_token):
        # fetch profile data for the given access_token
        user = User.get_user_by_id(id=access_token)
        # check if access_token is valid/ user exist
        if (not user):
            resp = jsonify({'message': 'Invalid access token.'})
            resp.status_code = 401
        else:
            # resp.message = 'Successfully retrieved profile data'
            resp = jsonify({
                'message': 'Successfully retrieved profile data.',
                'data': user.object_to_json()
            })
            resp.status_code = 201

    # return response message along with data and response code
    return resp


# # ~~~~~~~~~~~~~~~~~~~~~~~~~ OTP START ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @main.route('/otp', methods=['POST'])
# def otp_post():
#     # get payload data
#     payload_data = json.loads(request.data)
#     contact_number = payload_data.get('contact_number')
#     # check if mobile number present
#     if (not contact_number):
#         return jsonify({
#             "message": "Contact number not found.",
#             "status_code": 404
#         })

#     # validate mobile number

#     # check the number of times otp request for a mobile number

#     # if its crossing a certain number request, then reject the request

#     # generate random OTP of 6-digits

#     # get hashed(generated OTP)

#     # return hashed_otp
#     pass


# # ~~~~~~~~~~~~~~~~~~~~~~~~~ OTP END ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
