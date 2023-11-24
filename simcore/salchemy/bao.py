from . import config as config_vars
from .dao import SalchemyDAO

class SalchemyBAO(SalchemyDAO):

    def __init__(self, config_dict=None):
        # create an instance of the SalchemyDAO()
        SalchemyDAO.__init__(self)

        ########################################################
        # now check the configuration parameters
        # if all is well then attempt to establish a connection
        ########################################################
        if self.validate_config(config_dict) is True:
            self._establish_connection(config_dict)

    def delete(self, q_object=None):

        # delete the records
        try:
            results = q_object.one()
            retval = self._delete_object(results)
        except Exception as e:
            raise e
            #retval = False
        self.close()
        return retval
    ###################################
    # Input: None
    # Output: True/False
    # Logic: checks if sqlalchemy
    # is able to perform a query against the database
    ###################################
    def check_connection(self):
        print("inside check connection")
        retval = False

        try:
            retval = self._is_connected()
        except Exception:
            retval = False
        return retval

    ######################
    # input: dictionary
    # output: True/False
    ######################

    def validate_config(self, config_dict = None):
        retval = True
        if config_dict is None:
            return False

        if 'connection_type' in config_dict:
            if config_dict['connection_type'] not in config_vars.VALID_CONNECTION_TYPE:
                retval = False

        if 'username' not in config_dict:
            retval = False

        if 'password' not in config_dict:
            retval = False

        if 'hostname' not in config_dict:
            retval = False

        if 'database' not in config_dict:
            retval = False

        return retval

    def select(self, query_object):
        results = self._execute_select(query_object)
        self.close()
        return results

    def save_commit(self):
        retval = False
        try:
            retval = self._save_commit()
        except Exception:
            raise
        self.close()
        return retval

    def save(self, query_object, commit_value=True):
        retval = False

        try:
            ##########################
            # will always return true
            ##########################
            retval = self._save_object(query_object, commit_value)
        except Exception as e:
            #############################################
            # will only hit here if self._save_object
            # raises and exception
            #############################################
            #retval = False
            raise e
        self.close()
        return retval

    def close(self):
        self._close_session()
        ####################################
        # check connection will return False
        # therefore we want he not of that
        ###################################
        retval = not(self.check_connection())
        return retval

    def disconnect(self):
        self._disconnect()
