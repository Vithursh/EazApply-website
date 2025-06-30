import csv

def receiveJobData():
    # Read data from the CSV file
    path_to_file = "/home/vithursh/Coding/EazApply/backend/File Data/job_data.csv"
    with open(path_to_file, 'r', newline='') as file:
        # Create a csv.reader object
        csv_reader = csv.reader(file)

        # Optionally, skip the header row if present
        header = next(csv_reader)
        print(f"Header: {header}")

        # Iterate over each row in the CSV file
        for row in csv_reader:
            print(row)