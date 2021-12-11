import database


def check_user_exist(user_id: str):
    """
    Check database contain given user information.
    :param user_id: user account number
    :return: True if exist
    """
    return database.exist_in_database('User_ID', user_id, 'User')


def generate_new_uid():
    query_str = f'SELECT COUNT(*) FROM User;'
    s, q_result = database.fetch_query(query_str)
    curr_user_count = q_result[0][0]
    return str(curr_user_count + 1)


def add_user(user_name: str, password: str):
    """
    Create user with empty favourite list.
    :param password: login password
    :param user_name: login user name
    :return: user account number(user id)
    """
    new_id = generate_new_uid()
    insert_str = f"INSERT INTO User " \
                 f"VALUES({new_id},\'{user_name}\', \'{password}\');"
    success, response = database.execute_query(insert_str)
    return new_id, success


def change_password(user_id: str, new_password: str):
    """
    Change password of user with given uid
    :param new_password: new password
    :param user_id: request user id
    :return: True if successfully change password
    """
    execute_str = f"UPDATE User " \
                  f"SET Password = '{new_password}' " \
                  f"WHERE User_ID = {user_id};"
    return database.execute_query(execute_str)


def change_user_name(user_id: str, new_name: str):
    """
    Change user_name of user with given uid
    :param new_name: new name
    :param user_id: request user id
    :return: True if successfully change user_name
    """
    execute_str = f"UPDATE User " \
                  f"SET Name = '{new_name}' " \
                  f"WHERE User_ID = {user_id};"
    return database.execute_query(execute_str)


def get_user_favourite(user_id: str):
    fetch_str = f'SELECT Champion_ID FROM Favourite WHERE User_ID = {user_id};'
    s, q_result = database.fetch_query(fetch_str)
    if len(q_result) == 0:
        return [], []
    in_str = '('
    favourite_list = []
    for i in q_result:
        in_str += f"{str(i[0])},"
        favourite_list.append(i[0])
    in_str = in_str[:-1] + ')'
    fetch_str = f'SELECT * FROM Champion WHERE Champion_ID IN {in_str};'
    s, q_result = database.fetch_query(fetch_str)
    column_name = ['Champion_ID', 'Name', 'Class', 'Resource', 'Range_Type', 'Region', 'Adaptive_Type',
                   'Background_Story', 'Rating_ID', 'Skill_ID', 'Image_Url', 'Main_Page_Url']
    formatted_result = database.format_query_result(column_name, q_result)
    return favourite_list, formatted_result


def get_user_info(user_id: str):
    if check_user_exist(user_id) is False:
        return None
    user_info = {'User_ID': user_id}
    query_str = f'SELECT * FROM User WHERE User_ID = {user_id};'
    s, q_result = database.fetch_query(query_str)
    user_info['Name'] = q_result[0][1]
    user_info['Password'] = q_result[0][2]
    favourite_list, favourite_detail = get_user_favourite(user_id)
    user_info['Favourite'] = favourite_list
    user_info['Favourite_Detail'] = favourite_detail
    return user_info


def add_favourite(user_id: str, champion_id: str):
    """
    Add favourite champion to favourite_list of user with given id
    :param champion_id: added champion's id
    :param user_id: request user id
    :return: True if successfully add champion or champion already exist
    """
    insert_str = f"INSERT INTO Favourite " \
                 f"VALUES({user_id},{champion_id});"
    success, response = database.execute_query(insert_str)
    return success


def remove_favourite(user_id: str, champion_id: str):
    """
    Remove favourite champion from favourite_list of user with given id
    :param champion_id: champion's id to remove
    :param user_id: request user id
    :return: True if successfully remove champion
    """
    favourite_list, detail = get_user_favourite(user_id)
    if int(champion_id) not in favourite_list:
        return False
    delete_str = f"DELETE FROM Favourite " \
                 f"WHERE User_ID = {user_id} AND Champion_ID = {champion_id};"
    success, response = database.execute_query(delete_str)
    return success


if __name__ == '__main__':
    # test_id, test_response = add_user('Allen', '123')
    # test_Result = check_user_exist('2')
    # test_id, test_response = change_user_name('2', 'Allen1')
    # suc = add_favourite('2', '1')
    result = get_user_info('1')
    print(result)