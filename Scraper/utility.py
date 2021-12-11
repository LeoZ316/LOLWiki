import json
import csv
import string


def export_to_json(file_path, export_dict):
    with open(file_path, 'w') as export_file:
        json.dump(export_dict, export_file, indent=2)
        print("data has been export to " + file_path)


def load_json(file_path):
    with open(file_path) as loaded_file:
        data = json.load(loaded_file)
        return data


def transfer_match_up_json(match_up_file, name_id_file):
    match_up_data = load_json(match_up_file)
    name_id_data = load_json(name_id_file)
    result = []
    for data in match_up_data:
        curr_result = {}
        first_name = data['First_Champion_ID']
        second_name = data['Second_Champion_ID']
        if first_name == 'Kled':
            first_name = "Kled & Skaarl"
        if first_name == 'Nunu & Willump':
            first_name = 'Nunu'
        if second_name == 'Kled':
            second_name = "Kled & Skaarl"
        if second_name == 'Nunu & Willump':
            second_name = 'Nunu'
        win_rate = data['Win_Rate']
        curr_result['First_Champion_ID'] = name_id_data[first_name]
        curr_result['Second_Champion_ID'] = name_id_data[second_name]
        curr_result['Win_Rate'] = win_rate
        result.append(curr_result)
    export_to_json('json_file/match_up_win_rate.json', result)


def json_to_csv():
    with open('json_file/match_up_win_rate.json') as json_file:
        json_data = json.load(json_file)

    data_file = open('json_file/match_up_win_rate.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)

    count = 0
    for data in json_data:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())

    data_file.close()


if __name__ == '__main__':
    # transfer_match_up_json('json_file/champion_matchup_win_rate.json', 'json_file/champion_name_id.json')
    json_to_csv()

