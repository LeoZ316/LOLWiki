from app import *
from flask import request
from flask_restful import Resource, abort
import database
import utility
import user_system


@app.route('/')
def homepage():
    return {'Query Result': 'Home Page'}, 200


@app.route('/champion/image', methods=['GET'])
def get_champion_image():
    """
    Get id,name,image_url of all champions
    :return: query result
    """
    column_name = ["Champion_ID", "Name", "Image_Url"]
    status, query_result = database.fetch_query(f'SELECT Champion_ID,Name,Image_Url '
                                                f'FROM Champion; ')
    formatted_result = database.format_query_result(column_name, query_result)
    return {'Query Result': formatted_result}, 200


@app.route('/champion/counter', methods=['GET'])
def get_champion_counter():
    """
    Get Champion_ID, Against_Champion_ID, Against_Champion_Name, Image_URL, Counter Relation
    :return: query result
    """
    column_name = ["Champion_ID", "Against_Champion_ID", "Against_Champion_Name", "Against_URL", "Counter_Relation"]
    request_id = request.args.get('id')
    status, query_result = database.fetch_query(f"CALL Get_Counter_Relation({request_id});")
    formatted_result = database.format_query_result(column_name, query_result)
    return {'Query Result': formatted_result}, 200


@app.route('/champion/complete/info', methods=['GET'])
def get_champion_complete_info():
    """
    Get complete info including rating / skill of a champion
    :return: query result
    """
    column_name = ['Champion_ID', 'Rating_ID', 'Skill_ID', 'Name', 'Class', 'Resource', 'Range_Type', 'Region',
                   'Adaptive_Type',
                   'Background_Story', 'Image_Url', 'Main_Page_Url', 'Skill_Innate',
                   'Skill_Q', 'Skill_W', 'Skill_E', 'Skill_R', 'Damage', 'Toughness', 'Control', 'Mobility', 'Utility']
    request_id = request.args.get('id')
    query_str = f'SELECT * ' \
                f'FROM Champion NATURAL JOIN Skill NATURAL JOIN Rating ' \
                f'WHERE Champion_ID = {request_id};'
    status, query_result = database.fetch_query(query_str)
    formatted_result = database.format_query_result(column_name, query_result)
    return {'Query Result': formatted_result}, 200


# e.g. http://127.0.0.1:5000/matchup/against?Second_Champion_ID=0&Position_Name=Top
@app.route('/matchup/against', methods=['GET'])
def get_matchup_against():
    """
    First advanced query
    :return: query result
    """
    sc_id = request.args.get('Second_Champion_ID')
    if not sc_id:
        return {'error_message': 'Second_Champion_ID is not found'}, 400
    p_name = request.args.get('Position_Name')
    if not p_name:
        return {'error_message': 'Position_Name is not found'}, 400

    column_name = ["Champion_ID", "Name", "Win_Rate", "Image_Url", "Range_Type"]
    status, query_result = database.fetch_query(f'SELECT c.Champion_ID, c.Name, d.Win_Rate, c.Image_Url, c.Range_Type '
                                                f'FROM Champion AS c JOIN (SELECT Champion_ID, Win_Rate '
                                                f'FROM Champion_Position p JOIN Match_Up_Win_Rate w on p.Champion_ID = w.First_Champion_ID '
                                                f'WHERE Second_Champion_ID = {sc_id} '
                                                f'GROUP BY Position_Name, Champion_ID '
                                                f'HAVING Position_Name = "{p_name}" '
                                                f') AS d ON c.Champion_ID = d.Champion_ID '
                                                f'ORDER BY Win_Rate DESC '
                                                f'LIMIT 15;')
    formatted_result = database.format_query_result(column_name, query_result)
    return {'Query Result': formatted_result}, 200


# e.g. http://127.0.0.1:5000/matchup/recommendation?Position_Name=Top&c1_ID=1&c2_ID=2&c3_ID=3&c4_ID=4
@app.route('/matchup/recommendation', methods=['GET'])
def get_matchup_recommendation():
    """
    Second advanced query
    :return: query result
    """
    p_name = request.args.get('Position_Name')
    if not p_name:
        return {'error_message': 'Position_Name is not found'}, 400
    id_list = [-1, -1, -1, -1]
    for i in range(len(id_list)):
        id_list[i] = request.args.get(f'c{i + 1}_ID')
        if not id_list[i]:
            return {'error_message': f'c{i + 1}_ID is not found'}, 400

    # find rating attribute with min value in the sum of value of rating attributes for 4 champions
    count_list = [0, 0, 0, 0, 0]
    rating_attr = ["Damage", "Toughness", "Control", "Mobility", "Utility"]
    for curr_id in id_list:
        # for each Champion_ID, select ratings
        status, query_result = database.fetch_query(f'SELECT Damage, Toughness, Control, Mobility, Utility '
                                                    f'FROM Rating '
                                                    f'WHERE Rating_ID = {curr_id};')
        formatted_result = database.format_query_result(rating_attr, query_result)
        # print(formatted_result)
        for rating_attr_i in range(5):
            # for each rating value of current champion, add count
            count_list[rating_attr_i] += formatted_result[0][rating_attr[rating_attr_i]]
    # find min
    min_value = min(count_list)
    min_index = count_list.index(min_value)
    r_field = rating_attr[min_index]

    # recommend champion
    column_name = ["Champion_ID", "Name", "Damage", "Toughness", "Control", "Mobility", "Utility", "Image_Url"]
    status, query_result = database.fetch_query(
        f'SELECT c.Champion_ID, c.Name, d.Damage, d.Toughness, d.Control, d.Mobility, d.Utility, c.Image_Url '
        f'FROM Champion c NATURAL JOIN (SELECT * '
        f'FROM Champion_Position p JOIN Rating r on p.Champion_ID = r.Rating_ID '
        f'WHERE p.Position_Name = "{p_name}" AND r.{r_field} >= ALL(SELECT {r_field} '
        f'FROM Champion_Position p1 JOIN Rating r1 ON p1.Champion_ID = r1.Rating_ID '
        f'WHERE Position_Name = "{p_name}") '
        f'ORDER BY r.{r_field} DESC) as d '
        f'LIMIT 15;')
    formatted_result = database.format_query_result(column_name, query_result)
    for removed_id in id_list:
        for idx, result in enumerate(formatted_result):
            if result['Champion_ID'] == int(removed_id):
                del formatted_result[idx]
    result_dict = {"need": r_field, "recommendation": formatted_result}
    return {'Query Result': result_dict}, 200


class Champion(Resource):
    """
    Resource class that handle "/champion" request
    """
    table_name = "Champion"
    id_name = 'Champion_ID'
    # column_name = database.fetch_table_column_name(table_name)
    column_name = ['Champion_ID', 'Name', 'Class', 'Resource', 'Range_Type', 'Region', 'Adaptive_Type',
                   'Background_Story', 'Rating_ID', 'Skill_ID', 'Image_Url', 'Main_Page_Url']

    def get(self):
        """
        Get 1 champion info according to id or all champion info
        :return: query result from database or error message
        """
        got_id = utility.check_valid_id()
        got_name = request.args.get('name', None)
        if got_id is None and got_name is None:
            status, query_result = database.fetch_query(f'SELECT * '
                                                        f'FROM {self.table_name};')
        else:
            if got_name is None:
                status, query_result = database.fetch_query(f'SELECT * '
                                                            f'FROM {self.table_name} '
                                                            f'WHERE {self.id_name}={got_id};')
            else:
                status, query_result = database.fetch_query(f'SELECT * '
                                                            f'FROM {self.table_name} '
                                                            f"WHERE Name=\"{got_name}\";")
            if len(query_result) == 0:
                abort(404, error_message="Champion not exists")
        formatted_result = database.format_query_result(self.column_name, query_result)
        return {'Query Result': formatted_result}, 200

    def put(self):
        """
        Update a champion info by id
        :return: success response or error message
        """
        utility.check_json_content_type()
        got_id = utility.check_valid_id()
        if got_id is None:
            abort(404, error_message="Query arg id does not exist")
        else:
            set_query = utility.generate_update_query(self.column_name)
            status, result = database.execute_query(f'UPDATE {self.table_name} '
                                                    f'{set_query} '
                                                    f'WHERE {self.id_name}={got_id};')
            if status is False:
                return {"error_message": result}, 404
        return {"Response": "Put success"}, 200

    def post(self):
        """
        Insert 1 row to champion table
        :return: success response or error message
        """
        utility.check_json_content_type()
        got_id = utility.check_valid_id()
        if got_id is None:
            abort(400, error_message="Query arg id does not exist")
        else:
            if database.exist_in_database(self.id_name, got_id, self.table_name) is True:
                abort(400, error_message="Row with this id already exist.")
            insert_query = utility.generate_insert_query(self.column_name, self.id_name, got_id, self.table_name)
            status, result = database.execute_query(insert_query)
            if status is False:
                print(result)
                return {"error_message": result}, 200
        return {"Response": "Post success"}, 200

    def delete(self):
        """
        Delete 1 row from champion table
        :return: success response or error message
        """
        got_id = utility.check_valid_id()
        if got_id is None:
            abort(404, error_message="Query arg id does not exist")
        else:
            if database.exist_in_database(self.id_name, got_id, self.table_name) is False:
                abort(404, error_message="Row with this id doesn't exist.")
            status, result = database.execute_query(f'DELETE FROM {self.table_name} '
                                                    f'WHERE {self.id_name}={got_id};')
            if status is False:
                return {"error_message": result}, 404
        return {"Response": "Delete success"}, 200


api.add_resource(Champion, "/champion")


@app.route('/user/add', methods=['POST'])
def sign_up_user():
    """
    Add one user to user system
    :return: Success response or error message
    """
    sign_up_dict = {'user_name': request.args.get('name', None), 'password': request.args.get('password', None)}
    if sign_up_dict['user_name'] is None:
        return {"Error_message": "Provided body is invalid"}, 400
    if sign_up_dict['password'] is None:
        return {"Error_message": "Provided body is invalid"}, 400
    uid, success = user_system.add_user(sign_up_dict['user_name'], sign_up_dict['password'])
    if success:
        return {'Response': f'Your uid is {uid}. Please remember it.'}, 200
    return {"Error_message": "Failed to add user"}, 404


@app.route('/user/password', methods=['GET'])
def get_user_password():
    """
    Get user password with given uid
    :return: password or error message
    """
    request_uid = utility.check_valid_user_id()
    if request_uid is None:
        return {"Error_message": "Query arg id is not valid"}, 400
    user_info = user_system.get_user_info(request_uid)
    password = user_info['Password']
    return {'Query Result': password}, 200


@app.route('/user/password', methods=['PUT'])
def change_user_password():
    """
    Change user password with given uid
    :return: Success response or error message
    """
    uid = utility.check_valid_user_id()
    if uid is None:
        return {"Error_message": "Query arg id is not valid"}, 400
    new_password = request.args.get('password', None)
    if new_password is None:
        return {"Error_message": "Query arg password not exist"}, 400
    user_system.change_password(uid, new_password)
    return {'Response': f'user with uid {uid} changes password to {new_password}'}, 200


@app.route('/user/name', methods=['PUT'])
def change_user_name():
    """
    Change user name with given uid
    :return: Success response or error message
    """
    uid = utility.check_valid_user_id()
    if uid is None:
        return {"Error_message": "Query arg id is not valid"}, 400
    new_name = request.args.get('name', None)
    if new_name is None:
        return {"Error_message": "Query arg password not exist"}, 400
    user_system.change_user_name(uid, new_name)
    return {'Response': f'user with uid {uid} changes name to {new_name}'}, 200


@app.route('/user/info', methods=['GET'])
def get_user_info():
    """
    Get all user information with given id
    :return: query result or error message
    """
    request_uid = utility.check_valid_user_id()
    if request_uid is None:
        return {"Error_message": "Query arg id is not valid"}, 400
    user_info = user_system.get_user_info(request_uid)
    return {'Query Result': user_info}, 200


@app.route('/user/favourite', methods=['PUT'])
def add_user_favourite():
    """
    Add 1 favourite champion
    :return: Success response or error message
    """
    info_list = utility.check_valid_favourite_arg()
    if info_list is None:
        return {"Error_message": "Query arg user_id/champion_id are not valid"}, 400
    user_system.add_favourite(info_list[0], info_list[1])
    return {'Response': f"Champion {info_list[1]} added to user {info_list[0]} favourite"}, 200


@app.route('/user/favourite', methods=['DELETE'])
def remove_user_favourite():
    """
    Remove 1 favourite champion
    :return: Success response or error message
    """
    info_list = utility.check_valid_favourite_arg()
    if info_list is None:
        return {"Error_message": "Query arg user_id/game_id are not valid"}, 400
    status = user_system.remove_favourite(info_list[0], info_list[1])
    if status is False:
        return {"Error_message": "User doesn't have this champion in favourite list"}, 400
    return {'Response': f"Champion {info_list[1]} remove from user {info_list[0]} favourite"}, 200
