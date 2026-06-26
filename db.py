#gets all capabilities a device must have for a task to be assigned

#select * from task_required_capabilities trc where trc.task_id == id

import sqlite3
from threading import Event

database = sqlite3.Connection('latest.db', autocommit=True, check_same_thread=False)
databaseWriteInProgress = Event()

def __get_database_readable():
    return not databaseWriteInProgress.is_set()

def get_capabilities():
    print('waiting to access database')

    if __get_database_readable():
        print('get all capabilities from database')

        cursor = database.cursor()
        result = cursor.execute("select * from capability")
        results = result.fetchall()
        cursor.close()

        payload = []

        if results is not None:
            payload = [{"id": item[0], "name": item[1]} for item in results]
        
        if payload.count != 0:
            print(payload)

    return payload
        
def get_all_prefixes():
    if __get_database_readable():
        print(f"get all prefixes from database")

        cursor = database.cursor()
        result = cursor.execute("select id, prefix, description from device_type ORDER BY prefix ASC")
        results = result.fetchall()
        cursor.close()

        payload = []

        if results is not None:
            payload = [{"id": item[0], "name": item[1], "description":item[2]} for item in results]
        
        if payload.count != 0:
            print(payload)

    return payload

def get_prefixes(prefix:str = None, manufacturer:str = None):
    payload = []
    if prefix is not None:
        print(f"get device prefix {prefix} details from database")
        if manufacturer is not None:
            print(f"get device prefixes {prefix} from database where manufacturer {manufacturer}")
    else:
        payload = get_all_prefixes()

    return payload

def get_all_models():
    print('waiting to access database')

    if __get_database_readable():
        print(f"get all models from database")

        cursor = database.cursor()
        result = cursor.execute("select * from device_model_control_types")
        results = result.fetchall()
        cursor.close()
        
        payload = []

        if results is not None:
            payload = [{"id": item[2], "name": item[3],  "manufacturer_name":item[1], "manufacturer_id":item[0], "control_type_id":item[4], "control_type_name":item[5]} for item in results]
        
        if payload.count != 0:
            print(payload)

    return payload

def get_models_by_manufacturer(manufacturer):
    return []

def get_models(model: str = None, manufacturer:str = None):
    payload = []

    if model is not None:  
        if manufacturer is not None:
            print(f"get device model {model} details from database where manufacturer {manufacturer}")
        else:
            print(f"get device model {model} details from database")
    else:
        payload = get_all_models()
    
    return payload

def get_manufacturers():
    print('waiting to access database')

    if __get_database_readable():
        print(f"get all manufacturers from database")

        cursor = database.cursor()
        result = cursor.execute("select * from device_manufacturer")
        results = result.fetchall()
        cursor.close()

        payload = []

        if results is not None:
            payload = [{"id": item[0], "name": item[1]} for item in results]
        
        if payload.count != 0:
            print(payload)

    return payload

def get_control_types():
    print('waiting to access database')

    if __get_database_readable():
        print('get all controltypes from database')

        cursor = database.cursor()
        result = cursor.execute("select * from control_type")
        results = result.fetchall()
        cursor.close()

        payload = []

        if results is not None:
            payload = [{"id": item[0], "name": item[1]} for item in results]
        
        if payload.count != 0:
            print(payload)

    return payload

def get_tasks():
    print('waiting to access database')

    if __get_database_readable():
        print('get all tasks from database')

        cursor = database.cursor()
        result = cursor.execute("select * from task")
        results = result.fetchall()
        cursor.close()

        payload = []

        if results is not None:
            payload = [{"id": item[0], "name": item[1]} for item in results]
        
        if payload.count != 0:
            print(payload)

    return payload