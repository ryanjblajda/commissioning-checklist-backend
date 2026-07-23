#gets all capabilities a device must have for a task to be assigned

#select * from task_required_capabilities trc where trc.task_id == id

import sqlite3
from threading import Event

import model

databaseWriteInProgress = Event()
database = sqlite3.Connection('latest.db', autocommit=True, check_same_thread=False)


def __get_database_readable():
    return not databaseWriteInProgress.is_set()

def add_device(payload:model.NewDevicePayload):
    success = False
    print(payload)
    if payload.manufacturer_id != 0 and payload.prefix_id != 0:
        print('waiting to access database')
        if __get_database_readable():
            print('checking if desired model exists in the database')

            cursor = database.cursor()
            result = cursor.execute("select * from device_model dm where dm.model == ?", (payload.model, ))
            results = result.fetchall()

            if results is not None:
                if len(results) != 0:
                    print('model found in database => cannot add')
                else:
                    print('no model found => attempting to add new device')
                    success = True
        
                    databaseWriteInProgress.set()

                    added = False
                    try:
                        cursor.execute("insert into device_model (manufacturer_id, model, device_type_id) values (?, ?, ?)", (payload.manufacturer_id, payload.model, payload.prefix_id, ))
                        database.commit()
                        added = True
                        print(f"added new device {payload.model}");
                    except Exception as msg:
                        database.rollback()
                        print(msg)
                    
                    if added:
                        id = 0

                        result = cursor.execute("select * from device_model where model = ?", (payload.model, ))
                        results = result.fetchall()
                        id = int(results[0][0])
                        print(f"fetched new device id {id}")

                        if id != 0:
                            #print(payload.capabilities)
                            for capability in payload.capabilities:
                                try:
                                    cursor.execute("insert into device_model_capability (device_model_id, capability_id) values (?, ?)", (id, capability, ))
                                    database.commit()
                                    print(f"added capability {capability}")
                                except Exception as msg:
                                    print(f'exception {msg}')
                                    database.rollback()
                                    break

                    databaseWriteInProgress.clear()
    else:
        print('cannot add device without valid manufacturer and prefix id!')

    return success

def add_capability(payload:model.NewItemPayload):
    return None, None

def add_prefix(payload:model.NewItemPayload):
    success = False
    reason = "unknown"
    print("add prefix")

    if __get_database_readable():
        databaseWriteInProgress.set()
        cursor = database.cursor()
        try:
            cursor.execute("insert into device_type (prefix, description) values (?, ?)", (payload.name, payload.description, ))
            success = True
        except Exception as msg:
            reason = str(msg)
        databaseWriteInProgress.clear()
    print(f"result: {success} {reason}")
    return success, reason

def add_model(payload:model.NewItemPayload):
    success = False
    reason = "unknown"
    print("add model")
    return success, reason

def add_manufacturer(payload:model.NewItemPayload):
    success = False
    reason = "unknown"
    print("add manufacturer")
    return success, reason

def add_control(payload:model.NewItemPayload):
    success = False
    reason = "unknown"
    print("add control")
    return success, reason

def add_task(payload:model.NewItemPayload):
    success = False
    reason = "unknown"
    print("add task")
    return success, reason

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
            payload = [{"id": item[0], "name": item[1], "description": item[2]} for item in results]
        
        if payload.count != 0:
            print(payload)

    return payload