import json
from app import db
import datetime


# User model class
class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    create_datetime = db.Column(db.String(50))
    update_datetime = db.Column(db.String(50))

    def __init__(self, id, email, password, create_datetime,
                 update_datetime, ):
        if (id is not None):
            self.id = id
        self.email = email
        self.password = password
        self.create_datetime = create_datetime
        self.update_datetime = update_datetime

    # to return class data as json object
    def object_to_json(self):
        json_obj = self.__dict__  # This gives an extra '_sa_instance_state' field,which is not serialzable.
        json_obj.pop('_sa_instance_state')  # remove the '_sa_instance_state'
        return json_obj

    # CREATE
    def create_user(user):
        # logger.info("create_user...")
        db.session.add(user)
        db.session.commit()


    
    # get_user_by_email
    def get_user_by_email(email):
        # Query the user with the id
        fetched_user = db.session.query(User).filter(User.email == email).first()
        return fetched_user
    
    # get_user_by_id
    def get_user_by_id(id):
        # Query the user with the id
        fetched_user = db.session.query(User).filter(User.id == id).first()
        return fetched_user


    # UPDATE
    def update_user(user):
        # logger.info("update_user...")

        # Query the user with the id
        fetched_user = db.session.query(User).filter(User.id == user.id).one()

        # Modify the values of the columns
        fetched_user.email = user.email
        fetched_user.password = user.password
        fetched_user.update_datetime = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        # COMMIT the transaction to update the data in the database
        db.session.commit()

    # # query.all()
    # def get_users():
    #     # logger.info("get_users...")

    #     users = User.query.all()
    #     # users = db.session.query(User).all()
    #     users = [i.object_to_json() for i in users]
    #     return users
    
    
    
    # # # DELETE
    # # def delete_user(user):
    # #     fetched_user = db.session.query(User).filter(User.id == user.id).one()
    # #     db.session.delete(fetched_user)
    # #     db.session.commit()
    
