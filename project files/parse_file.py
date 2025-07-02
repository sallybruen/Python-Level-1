import json
import os


def get_json_content(file):
    """
        Read the JSON file that was passed in, get the data in the file.
        Save the data in a list of dictionaries, where each dictionary
        is the employee entry.
    """
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)     # load JSON data
        if type(data) is list:     # return if correct type
            return data
        print(f'Warning: The file {file} does not contain a list of employees.')
        return []   # return empty list if file is not a list of dictionaries


def generate_email(first_name, last_name):
    """
        Generate the email address for the employee entry to follow the format:
        <first letter of first name><last name>@comp.com
    """
    email_first_letter = first_name[0].lower()      # first letter lowercase
    email_last_name = last_name.lower()         # last name lowercase
    company_email = '@comp.com'
    employee_email = email_first_letter + email_last_name + company_email
    return employee_email


def generate_formatted_file(emp_list, orig_path):
    """
        For each file, save its contents to a separate new JSON file in the
        same folder where the original file is located.
        Add extension '_formatted.json' to the new file name.
    """
    # split directory from original filename
    directory, original_filename = os.path.split(orig_path)
    # remove extension from orig filename
    file_name_without_ext, _ = os.path.splitext(original_filename)

    # new file name with "_formatted.json" extension
    new_file_name = f"{file_name_without_ext}_formatted.json"
    # join directory to new file name for new path
    new_file_path = os.path.join(directory, new_file_name)

    # write formatted list of dictionaries into new JSON file
    with open(new_file_path, 'w', encoding='utf-8') as f:
        json.dump(emp_list, f, indent=4)


def generate_salary(job_id, state):
    """
        Generate the salary of the employee based on their department,
        role and state.
        Where expensive states get an extra 1.5% and managers get an
        extra 5%. Managers in expensive states get 6.5% increase
    """
    department_salary = {'SA': 60000,
                         'HR': 70000,
                         'IT': 80000}
    expensive_states = {'NY', 'CA', 'OR', 'WA', 'VT'}

    # separate department and role
    department, role = job_id.split("_")
    # assign salary based on department
    calculated_salary = department_salary.get(department, 0)

    if role == 'MNG' and state in expensive_states:
        # manager in expensive state = 6.5% increase
        calculated_salary *= 1.065
    elif state in expensive_states:
        # expensive states = 1.5% increase
        calculated_salary *= 1.015
    elif role == 'MNG':
        # mangers not in expensive state = 5% increase
        calculated_salary *= 1.05

    return round(calculated_salary)         # return rounded int value


def process_each_emp(emp_list):
    """
        Process each employee entry in a list of dictionaries and format it.
        Ensure the phone numbers and zip codes are valid, if not, skip the entry.
        Remove the last entry of the dictionary.
        Ensure proper casing for certain fields.
        Generate the company email and it to the dictionary.
        Generate the salary and add it to the dictionary.
    """
    list_of_employee_dictionaries = []
    format_fields = ["First Name", "Last Name", "Address Line 1",
                     "Address Line 2", "City", "Job Title"]    # keys to format

    for i in range(len(emp_list)):
        employees = emp_list[i]     # dictionary for this employee
        employees.popitem()         # remove the last entry of the dictionary

        # strip phone num and zip code, check if valid
        phone_number = employees.get('Phone Number', '').strip()
        valid_phone = validate_phone_number(phone_number)
        zip_code = employees.get('Zip Code', '').strip()
        valid_zip = validate_zip(zip_code)

        if valid_zip == 1 or valid_phone == 1:
            # skip employee entry if phone num or zip code invalid
            employees.clear()
            continue

        # add formatted zip code and phone num to dictionary
        employees['Zip Code'] = valid_zip
        employees['Phone Number'] = valid_phone

        for key in format_fields:       # format listed fields
            if type(employees[key]) is str and employees[key].strip():
                # split by spaces and remove extra spaces
                words = employees[key].strip().split()
                formatted_words = []
                for word in words:
                    if word[0].isdigit():
                        # If word starts with digit, lowercase
                        formatted_words.append(word.lower())
                    else:
                        # capitalize other words
                        formatted_words.append(word.capitalize())
                # join the formatted words
                employees[key] = " ".join(formatted_words)

        # get email address, add it to dictionary
        first_name = employees.get("First Name", "")
        last_name = employees.get("Last Name", "")
        employees['Company Email'] = generate_email(first_name, last_name)

        # get salary, add it to dictionary
        job_id = employees.get("Job ID", "")
        state = employees.get("State", "")
        employees['Salary'] = generate_salary(job_id, state)

        if employees:
            # add formatted employees to new dictionary
            list_of_employee_dictionaries.append(employees)

    return list_of_employee_dictionaries


def validate_phone_number(phone_number):
    """
        Check the given phone number to ensure it is valid.
        Return 1 and print message if not valid.
    """
    clean_number = []
    phone_number = phone_number.strip()     # remove spaces
    for num in phone_number:
        if num.isdigit():
            clean_number.append(num)        # add numbers only
        else:
            print(f"{phone_number} is not a valid US phone number, "
                  f"skipping this employee entry...")
            return 1

    if len(clean_number) != 10:     # incorrect length = invalid number
        print(f"{phone_number} is not a valid US phone number, "
              f"skipping this employee entry...")
        return 1
    return int(''.join(clean_number))       # return as int


def validate_zip(zip_code):
    """
        Check the given phone number to ensure it is valid.
        Return 1 and print message if not valid.
    """
    clean_zip_code = []
    zip_code = zip_code.strip()     # remove spaces

    for num in zip_code:
        if num.isdigit():           # add numbers only to clean list
            clean_zip_code.append(num)
        else:
            print(f"{zip_code} is not a valid US zip code, "
                  f"skipping this employee entry...")
            return 1

    if len(clean_zip_code) != 5:       # incorrect length = invalid zip code
        print(f"{zip_code} is not a valid US zip code, "
              f"skipping this employee entry...")
        return 1
    return int(''.join(clean_zip_code))     # return as int
