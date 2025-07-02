import os.path


def get_usr_input(msg):
    """
        Prompt the user with given message and get their input.
    """
    user_input = input(msg)
    return user_input


def check_path(file_path, data_files):
    """
        Check if the given path exists, if not display message.
        If path exists and is in folder, check the content of the folder.
        if the path exists and is already formatted, return 2.
        If path are valid, return them in a tuple.
    """
    if not os.path.exists(file_path):
        print(file_path + " does not exist.")
        return 1
    elif os.path.isdir(file_path):
        for file in os.listdir(file_path):
            check_path(os.path.join(file_path, file), data_files)
    else:
        if file_path.endswith("_formatted.json"):
            return 2        # error 2 as file is already formatted JSON
        elif file_path.endswith(".json"):
            data_files.append(file_path)            # add file path to list of valid files

    return tuple(data_files)
