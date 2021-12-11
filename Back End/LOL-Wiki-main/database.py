import os
from yaml import load, Loader
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError


def init_connect_engine():
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]
    pool = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername="mysql+pymysql",
                username=os.environ.get('MYSQL_USER'),
                password=os.environ.get('MYSQL_PASSWORD'),
                database=os.environ.get('MYSQL_DB'),
                host=os.environ.get('MYSQL_HOST')
            )
        )
    return pool


db = init_connect_engine()


def execute_query(query_str: str):
    try:
        conn = db.connect()
        exec_result = conn.execute(query_str)
        conn.close()
        return True, exec_result
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error.split("'")[1]
        return False, error


def fetch_query(query_str: str):
    try:
        conn = db.connect()
        query_result = conn.execute(query_str).fetchall()
        conn.close()
        return True, query_result
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return False, error


def fetch_table_column_name(table_name: str):
    conn = db.connect()
    query_str = f"select COLUMN_NAME " \
                f"from INFORMATION_SCHEMA.COLUMNS " \
                f"where TABLE_NAME=N'{table_name}';"
    query_result = conn.execute(query_str).fetchall()
    conn.close()
    column_name = []
    for result in query_result:
        column_name.append(result[0])
    print(column_name)
    return column_name


def format_query_result(column_name: list, query_result: list):
    if query_result is None or len(query_result) == 0:
        return {}
    formatted_result = []
    for result in query_result:
        info_dict = {}
        for idx, val in enumerate(column_name):
            info_dict[val] = result[idx]
        formatted_result.append(info_dict)
    return formatted_result


def exist_in_database(id_name: str, id_val: str, table_name: str):
    query_str = f"SELECT * " \
                f"FROM {table_name} " \
                f"WHERE {id_name}={id_val};"
    status, query_result = fetch_query(query_str)
    return len(query_result) != 0


def change_champion_img_url():
    id_name = 'Champion_ID'
    column_name = ['Champion_ID', 'Name', 'Image_Url']
    status, query_result = fetch_query(f'SELECT Champion_ID,Name,Image_Url '
                                       f'FROM Champion; ')
    formatted_result = format_query_result(column_name, query_result)
    for result in formatted_result:
        curr_id = result['Champion_ID']
        if curr_id == 19 or curr_id == 50 or curr_id == 59 or curr_id == 62 or curr_id == 95 or curr_id == 135:
            continue
        curr_url = result['Image_Url']
        new_url = curr_url.replace('/revision/latest/scale-to-width-down/46', '')
        query_str = f'UPDATE Champion SET Image_Url = \"{new_url}\" WHERE {id_name}={str(curr_id)};'
        print(query_str)
        status, query_result = execute_query(f'UPDATE Champion SET Image_Url = \"{new_url}\" WHERE {id_name}={str(curr_id)};')
        print(query_result)


if __name__ == '__main__':
    test_query = f'SELECT * ' \
                 f'FROM Champion NATURAL JOIN Skill NATURAL JOIN Rating ' \
                 f'WHERE Champion_ID = 1;'
    s, q_result = fetch_query(test_query)
    print(q_result)
    # status, result = execute_query("INSERT INTO Champion(Champion_ID, Range_Type) VALUES(180, 'SADA');")
    # print(result)
    # change_champion_img_url()