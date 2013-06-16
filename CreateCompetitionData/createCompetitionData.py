import csv
import numpy as np
import os

def expedia_personalized_sort_data_split_seed():
    return 255435345
    # raise NotImplementedError

def get_user_ids(raw_path):
    f = open(raw_path)
    # skip the header
    f.readline()
    reader = csv.reader(f, delimiter="\t")
    user_ids = list(set(row[0] for row in reader))
    f.close()
    return user_ids

def split_user_ids(user_ids, train_frac, valid_frac):
    index = np.arange(len(user_ids))
    np.random.seed(expedia_personalized_sort_data_split_seed())
    np.random.shuffle(index)
    train_end = int(train_frac*len(user_ids))
    valid_end = int((train_frac+valid_frac)*len(user_ids))
    train = index[:train_end]
    valid = index[train_end:valid_end]
    test =  index[valid_end:]

    user_ids_split = dict()

    for i in train:
        user_ids_split[user_ids[i]] = "train"
    for i in valid:
        user_ids_split[user_ids[i]] = "valid"
    for i in test:
        user_ids_split[user_ids[i]] = "test"

    return user_ids_split

def create_competition_data():
    data_path     = os.path.join(os.environ["DataPath"], "ExpediaPersonalizedSort")
    raw_path      = os.path.join(data_path, "Raw", "ExpediaPublicCompDataRaw2.txt")
    release_path  = os.path.join(data_path, "Release 1")
    train_path    = os.path.join(release_path, "train.csv")
    test_path     = os.path.join(release_path, "test.csv")
    solution_path = os.path.join(release_path, "solution.csv")

    f_train    = open(train_path, "w")
    f_test     = open(test_path, "w")
    f_solution = open(solution_path, "w")

    train_writer    = csv.writer(f_train,    lineterminator="\n")
    test_writer     = csv.writer(f_test,     lineterminator="\n")
    solution_writer = csv.writer(f_solution, lineterminator="\n")

    user_ids = get_user_ids(raw_path)
    user_ids_split = split_user_ids(user_ids, 0.6, 0.1)

    f_raw = open(raw_path)
    raw_reader = csv.reader(f_raw, delimiter="\t")
    header = raw_reader.next()
    train_writer.writerow(header[:23]+header[24:26])
    test_writer.writerow(header[:23])
    solution_writer.writerow(["user_id", "hotel_id", "relevance", "usage"])

    for row in raw_reader:
        if user_ids_split[row[0]] == "train":
            train_writer.writerow(row[:23]+row[24:26])
        else:
            test_writer.writerow(row[:23])
            relevance = str(min(2, 2*int(row[25])+int(row[24])))
            usage = "Public" if user_ids_split[row[0]] == "valid" else "Private"
            solution_row = [row[0], row[6], relevance, usage]
            solution_writer.writerow(solution_row)
    f_raw.close()
    f_train.close()
    f_test.close()
    f_solution.close()

if __name__=="__main__":
    create_competition_data()