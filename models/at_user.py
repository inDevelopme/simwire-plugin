from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from copy import deepcopy as __deepcopy
import uuid
Base = declarative_base()

class ATUser(Base):
    __tablename__ = 'at_user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    session_token = Column(String(45), unique=True)
    profile_id = Column( Integer)
    domain_id = Column(Integer)
    user_status_id = Column(String(50))
    password = Column(String(50))
    # user source type defaults to 5 for the time being
    # 5 = manually created account
    user_source_type_id = Column(Integer, default=5)
    allow_social_login = Column(Integer, default=0)


    def __init__(self):
        pass

    # used to perform updates
    def load_object(self, idict):
        if 'user_id' in idict:
            self.user_id = idict['user_id']

        if 'username' in idict:
            self.username = idict['username']

        if 'user_status_id' in idict:
            self.user_status_id = idict['user_status_id']

        if 'password' in idict:
            self.password = idict['password']

        if 'user_source_type_id' in idict:
            self.user_source_type_id = idict['user_source_type_id']

    ###########################################
    # Ensures data is returned as dictionary
    ###########################################



    #############################################
    # special case functions
    ############################################

    def load_session_token(self, idict):
        if 'session_token' in idict:
            self.session_token = idict['session_token']

    def randomize_session_token(self):
        self.session_token = uuid.uuid4()

    def __repr__(self):
        return '<ATUser %r>' % (self.user_id)