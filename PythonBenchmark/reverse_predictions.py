import csv
import data_io

def main():
    submission_path = data_io.get_paths()["submission_path"]
    reader = csv.reader(open(submission_path))
    reader.next() # skipping the header
    recommendations = [(int(row[0]), int(row[1]), -i)
        for i,row in enumerate(reader)]
    out_path = submission_path[:-4]+"Reversed.csv"
    data_io.write_submission(recommendations, submission_path=out_path)

if __name__=="__main__":
    main()