from flask import request
from flask_restful import abort
import json
import user_system
import database
import sqlalchemy


def export_to_json(file_path, export_dict):
    with open(file_path, 'w') as export_file:
        json.dump(export_dict, export_file, indent=2)
        print("data has been export to " + file_path)


def load_json(file_path):
    with open(file_path) as loaded_file:
        data = json.load(loaded_file)
        return data


def check_json_content_type():
    """
    Function that check if content type in request is set correctly
    """
    if request.content_type != "application/json":
        abort(415, error_message="Content type should be application/json")


def check_valid_id():
    """
    Function that check if id exist in query args and if id is valid
    """
    if 'id' not in request.args:
        return None
    try:
        got_id = int(request.args.get('id', None))
    except (TypeError, ValueError):
        abort(404, error_message="Id should be an integer")
        return None
    return str(got_id)


def generate_update_query(column_name: list):
    set_str = "SET "
    data = request.get_json()
    if len(data) == 0:
        abort(404, error_message="Not enough field argument is provided.")
    for key in data:
        if key not in column_name:
            abort(404, error_message="Invalid field name is provided.")
        else:
            set_str += f'{key} = {data[key]},'
    return set_str[:-1]


def generate_insert_query(column_name: list, id_name: str, got_id, table_name):
    insert_str = f'INSERT INTO {table_name} ({id_name},'
    value_str = f' VALUES ({got_id},'
    data = request.get_json()
    for key in data:
        if key not in column_name:
            abort(404, error_message="Invalid field name is provided.")
        insert_str += f'{key},'
        value_str += f'{data[key]},'
    insert_str = insert_str[:-1] + ')'
    value_str = value_str[:-1] + ');'
    return insert_str + value_str


def check_valid_sign_up_info():
    """
    Function that check if request body contain valid user name
    and password to sign up a user
    :return: valid input or None
    """
    data = request.get_json()
    if type(data) is not dict:
        return None
    else:
        if 'user_name' not in data:
            return None
        elif 'password' not in data:
            return None
    return data


def check_valid_user_id():
    """
    Function that check if given user id in query arg is valid
    :return: valid input or None
    """
    if 'id' not in request.args:
        return None
    request_id = request.args.get('id', None)
    if not user_system.check_user_exist(request_id):
        return None
    return request_id


def check_valid_favourite_arg():
    """
    Function that check if user provide a valid user id
    and a valid champion id. Used for favourite champion routes.
    :return: valid input or None
    """
    if 'user_id' not in request.args:
        return None
    if 'champion_id' not in request.args:
        return None
    user_id = request.args.get('user_id', None)
    champion_id = request.args.get('champion_id', None)
    if not user_system.check_user_exist(user_id):
        return None
    if not database.exist_in_database('Champion_ID', champion_id, 'Champion'):
        return None
    return [user_id, champion_id]



