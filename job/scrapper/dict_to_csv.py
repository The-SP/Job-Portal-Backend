import csv


def dict_to_csv(list_of_dicts, csv_filename):
    field_headings = list_of_dicts[0].keys()
    # Open a CSV file for writing
    with open(csv_filename, "w") as file:
        # Create a CSV writer
        writer = csv.DictWriter(file, fieldnames=field_headings)
        # Write the headers
        writer.writeheader()
        # Write the rows
        writer.writerows(list_of_dicts)
