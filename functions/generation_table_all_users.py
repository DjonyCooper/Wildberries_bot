def gen_table(all_user_list: dict):
    all_users = len(all_user_list)
    text_msg = f'Информация о всех ({all_users}) пользователях:\n\n'
    max_size_name = max([len(info[2]) for info in all_user_list])
    for info in all_user_list:
        len_name = len(info[2])
        new_name = info[2]
        if len_name < max_size_name:
            list_empty_size = max_size_name - len_name + 1
            empty_list = [''] * list_empty_size
            new_name = new_name + "  ".join(empty_list)
        text_msg += f'{info[0]} | {info[1]} | {new_name} | {info[3]}\n'
    return text_msg
