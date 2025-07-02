import sys
import usr_input
import parse_file


def error_handle(check_return):
    """
        Get return value from check_path, if value is 1, exit.
        If value is 2, display message and exit.
        If the tuple contains no path, message and exit.
    """
    if check_return == 1:           # path given is not valid
        sys.exit()
    elif check_return == 2:         # file given should not be processed
        print('The file provided is already processed.')
        sys.exit()
    elif isinstance(check_return, tuple) and not check_return:
        # if empty tuple
        print("There are no valid files to process in the folder provided.")
        sys.exit()


def print_output(num_files, num_emps):
    """
        Display the num of files and employees processed
    """
    print(f"============================================================\n"
          f"---------------------Processing Summary---------------------\n"
          f"============================================================\n"
          f"Number of files processed:   {num_files}\n"
          f"Number of employee entries\n"
          f" formatted and calculated:   {num_emps}")


def start_process(tup):
    """
        Calculate num of files and employees processed.
        Process each file and save the information in a new JSON file.
        Print the output
    """
    num_files = 0
    num_emps = 0

    for file_path in tup:       # loop through valid JSON files
        emp_list = parse_file.get_json_content(file_path)
        if emp_list:
            # format each employee entry
            formatted_emp_list = parse_file.process_each_emp(emp_list)
            # count num of employees processed
            num_emps += len(formatted_emp_list)
            # saves formatted lists
            parse_file.generate_formatted_file(formatted_emp_list, file_path)
            # counts num of files processed
            num_files += 1
    # print num of files and employees of processed
    print_output(num_files, num_emps)


def main():
    """
        Calls functions for the script to run as intended.
    """
    # get user intput with file path
    usr_input_string = usr_input.get_usr_input("Please enter "
                                               "the path of the file or the "
                                               "folder containing the files: ")
    data_files = []             # list to store valid file paths
    # check path of user input
    check_return = usr_input.check_path(usr_input_string, data_files)
    error_handle(check_return)      # check return value, sys.exit() if invalid

    if data_files:      # check data_files not empty
        start_process(tuple(data_files))     # start processing files


if __name__ == "__main__":
    main()
