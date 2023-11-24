from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from copy import deepcopy

class SalchemyDAO:

    __db = None
    __engine = None
    __conn = None
    __session = None
    __acceptable_db_type = ['mysql']

    # initialize the mailgun object for communication with mailgun
    def __init__(self):
        pass

    #########################
    # protected functions
    #########################
    def _establish_connection(self, config_dict):
        connection_string = config_dict['connection_type'] + '://' + config_dict['username'] + ':'

        #mysql://root:/[password]@localhost/
        connection_string += config_dict['password'] + '@' + config_dict['hostname'] + '/'

        #mysql://root:/[password]]@localhost/[database]
        connection_string += config_dict['database']

        self.__engine = create_engine(connection_string)
        self.__conn = self.__engine.connect()
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()


    def _close_session(self):
        self.__session.close()

    def _disconnect(self):
        self.__session = None
        self.__engine = None
        self.__conn = None

    def _execute_select(self, q_object= None):
        query = None

        # get base query
        if (q_object is None):
            raise NotImplementedError
        else:
            query = self.__session.query(q_object)

        return query
    def _save_commit(self):
        retval = False
        try:
            self.__session.commit()
            retval = True
        except Exception:
            raise

        return retval

    def _save_object(self, q_object=None, commit=True):
        # object must be of the form = (ATApp('Sandbox App', 'sbox_app_alias'))
        # this allows you to add an object before commit all that is already a part of the session
        retval = False
        if (q_object is not None):
            try:
                self.__session.add(q_object)
                if commit is True:
                    self.__session.commit()

                retval = True
            except Exception as e:  # catch all exceptions
                print(str(e))
                ################################################################
                # without this line the create/update that throw exceptions
                # will kill all possible future transactions
                ################################################################

                self.__session.rollback()
                raise (e)

        return retval

    def _delete_object(self, result_object=None):
        retval = False
        # object must be of the form = (ATApp('Sandbox App', 'sbox_app_alias'))
        # this allows you to add an object before commit all that is already a part of the session
        # results_object => must always be the results of performing select
        if (result_object is not None):
            try:
                self.__session.delete(result_object)
                self.__session.commit()
                retval = True
            except Exception as e:  # catch all exceptions
                print(str(e))
                raise (e)

        return retval

    ####################################
    # checks is a mock query can be
    # performed against the database
    ####################################

    def _is_connected(self):
        retval = False
        r = self.__session.query("1").from_statement("SELECT 1").all()
        if len(r) > 0:
            retval = True

        return retval

    def get_table_names(self):
        table_names = list()

        if self.__conn is not None:
            table_names = self.__engine.table_names()

        return table_names
