from sys import stderr
from datetime import datetime
import requests
import json
import csv


class ApiService:
    def __init__(self):
        try:
            self.todo = None
            self.storage_path = './storage/'
            self.json_data_url = 'https://jsonplaceholder.typicode.com/todos/'
        except Exception as e:
            print('There was an unexpected issue instantiating the ApiService class, contact the developer please')
            print('Issue described as:', e)

    def get_todo(self):
        """
        Gets the TODOs through an API rest call, if call was Ok
        sets its return into the 'todo' class variable
        :return: It has no return
        """
        try:
            # Pèrform the API call to the defined url in the 'json_data_url' class variable
            api_call = requests.get(self.json_data_url)

            # Verify the status_code of the api_call variable
            # if was Ok (200 code) then set the value in the 'todo' class variable
            # else report it (in this case, print it)
            if api_call.status_code == 200:
                self.todo = json.loads(api_call.text)
            else:
                print('The api call getting the TODOs failed, status code is:', api_call.status_code)
        except Exception as e:
            print('There was an unexpected issue getting the TODOs, contact the developer please')
            print('Issue described as:', e)

    def todo_to_csv(self):
        """
        Converts each TODO into a CSV file
        :return: It has no return
        """
        try:
            # Call the method to set the 'todo' class variable
            self.get_todo()

            # If previous call was successful the 'todo' class variable will have data
            if self.todo:
                # Get today date in the required format in README.md
                today_date = datetime.today().strftime("%Y_%m_%d")

                # The way this code is written is because the input format is known
                # otherwise, the keys for each dict will be retrieved
                # Doing this, the way is done is to save some execution time

                # Extract keys from the first dictionary to use as fieldnames
                fieldnames = list(self.todo[0].keys())

                # Iterate through the list of dictionaries
                for i, data in enumerate(self.todo):
                    # Define the CSV filename using today_date and the TODO id value
                    # Save it in the storage folder (so, include the route in the filename)
                    filename = f"{self.storage_path + today_date}_" + str(data["id"]) + ".csv"

                    # Quick fix: Since the language used is Python, the CSV were written with the
                    # completed field as the Python way, True or False, that is to say, first letter uppercase
                    # just fixed to all lowercase (as the traditional JSON)
                    data["completed"] = "true" if data["completed"] else "false"

                    # Write the CSV file
                    with open(filename, 'w', newline='') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        # Write header
                        writer.writeheader()
                        # Write data
                        writer.writerow(data)
            else:
                print('Failure: TODOs data is missed')
        except Exception as e:
            print('There was an unexpected issue converting the TODOs to CSV, contact the developer please')
            print('Issue described as:', e)

    def run(self):
        print('Running ApiService', file=stderr)
        self.todo_to_csv()
        print('Done ApiService', file=stderr)

        # TODO: follow README.md instructions
