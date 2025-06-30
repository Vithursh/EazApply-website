import csv

def receiveJobData():
    data = []
    index = 0
    # Read data from the CSV file
    path_to_file = "/home/vithursh/Coding/EazApply/backend/File Data/job_data.csv"
    with open(path_to_file, 'r', newline='') as file:
        # Create a csv.reader object with '|' as delimiter
        csv_reader = csv.reader(file, delimiter='|')

        # Optionally, skip the header row if present
        header = next(csv_reader)
        print(f"Header: {header}")

        # Iterate over each row in the CSV file
        for row in csv_reader:
            index += 1
            data.append({"id": index, "rank": row[0], "url": row[1], "paragraph": row[2]})
    
    return data