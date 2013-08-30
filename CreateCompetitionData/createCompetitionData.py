from __future__ import division
import csv
import heapq
from itertools import ifilter
import json
import numpy as np
import os

def expedia_personalized_sort_data_split_seed():
    seed_path = os.environ["SeedPath"]
    seeds = json.loads(open(seed_path).read())
    return seeds["ExpediaPersonalizedSortDataSplitSeed"]

def get_ids(raw_path):
    ids_dict = { "srch_ids" : set()
               , "site_ids" : set() 
               , "country_ids" : set()
               , "property_ids" : set()
               , "destination_ids" : set()}
    f = open(raw_path)
    # skip the header
    f.readline()
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        ids_dict["srch_ids"].add(row[0])
        ids_dict["site_ids"].add(row[2])
        ids_dict["country_ids"].add(row[3])
        ids_dict["country_ids"].add(row[6])
        ids_dict["property_ids"].add(row[7])
        ids_dict["destination_ids"].add(row[17])
    f.close()
    return ids_dict

def remap_ids(ids_dict):
    ids_map = {}
    for key in ids_dict:
        unique_ids = list(ids_dict[key])
        np.random.shuffle(unique_ids)
        ids_map[key] = {old_id: str(new_id+1) for new_id, old_id in enumerate(unique_ids)}
    return ids_map

def save_ids_map(ids_map, release_path):
    for key in ids_map:
        ids_list = [(old_id, ids_map[key][old_id]) for old_id in ids_map[key]]
        f = open(os.path.join(release_path, "%s_id_map.csv" % key), "w")
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["OldId", "NewId"])
        writer.writerows(ids_list)
        f.close()

def remap_row(ids_map, row):
    row[0] = ids_map["srch_ids"][row[0]]
    row[2] = ids_map["site_ids"][row[2]]
    row[3] = ids_map["country_ids"][row[3]]
    row[6] = ids_map["country_ids"][row[6]]
    row[7] = ids_map["property_ids"][row[7]]
    row[17] = ids_map["destination_ids"][row[17]]

def row_reader(ids_map, raw_reader):
    for row in raw_reader:
        remap_row(ids_map, row)
        yield row

def split_search_ids(search_ids, train_frac, valid_frac):
    index = np.arange(len(search_ids))
    np.random.shuffle(index)
    train_end = int(train_frac*len(search_ids))
    valid_end = int((train_frac+valid_frac)*len(search_ids))
    train = index[:train_end]
    valid = index[train_end:valid_end]
    test =  index[valid_end:]

    search_ids_split = dict()

    for i in train:
        search_ids_split[search_ids[i]] = "train"
    for i in valid:
        search_ids_split[search_ids[i]] = "valid"
    for i in test:
        search_ids_split[search_ids[i]] = "test"

    return search_ids_split

def row_order_key(row):
    return (int(row[0]), int(row[7]))

def row_filter(row, min_row=None):
    if min_row is None:
        return True
    return row_order_key(row) > row_order_key(min_row)

def create_competition_data():
    data_path              = os.path.join(os.environ["DataPath"], "ExpediaPersonalizedSort")
    raw_path               = os.path.join(data_path, "Raw", "ExpediaRaw.tsv")
    release_path           = os.path.join(data_path, "Release 1")
    train_path             = os.path.join(release_path, "train.csv")
    test_path              = os.path.join(release_path, "test.csv")
    solution_path          = os.path.join(release_path, "solution.csv")
    position_benchark_path = os.path.join(data_path, "Submissions", "positionBenchmark.csv")

    f_train              = open(train_path, "w")
    f_test               = open(test_path, "w")
    f_solution           = open(solution_path, "w")
    f_position_benchmark = open(position_benchark_path, "w")

    train_writer    = csv.writer(f_train,              lineterminator="\n")
    test_writer     = csv.writer(f_test,               lineterminator="\n")
    solution_writer = csv.writer(f_solution,           lineterminator="\n")
    position_writer = csv.writer(f_position_benchmark, lineterminator="\n")

    ids_dict = get_ids(raw_path)
    ids_map = remap_ids(ids_dict)
    save_ids_map(ids_map, release_path)
    search_ids_split = split_search_ids(ids_map["srch_ids"].values(), 0.6, 0.1)

    f_raw = open(raw_path)
    raw_reader = csv.reader(f_raw, delimiter="\t")
    header = raw_reader.next()
    reader = row_reader(ids_map, raw_reader) 
    train_writer.writerow(header)
    test_writer.writerow(header[:14] + header[15:51])
    solution_writer.writerow(["SearchId", "PropertyId", "Relevance", "Usage"])
    position_writer.writerow(["SearchId", "PropertyId"])

    rows_remaining = True
    min_row = None
    i=0
    batch_size = 500000

    # Ugly & slow way to do the sort with limited memory, but it works
    # If this was on Unix would save to a temp file and then use Unix sort
    while rows_remaining:
        remaining_rows = ifilter(lambda r: row_filter(r, min_row), reader)
        nsmallest = heapq.nsmallest(batch_size, remaining_rows, key=row_order_key)
        solution_set = [row for row in nsmallest if search_ids_split[row[0]] != "train"]
        for row in sorted(solution_set, key=lambda row: (int(row[0]), int(row[14]))):
            position_writer.writerow([row[0], row[7]])
        for row in nsmallest:
            if search_ids_split[row[0]] == "train":
                train_writer.writerow(row)
            else:
                test_writer.writerow(row[:14]+row[15:51])
                relevance = str(min(5, 5*int(row[-1])+int(row[-3])))
                usage = "Public" if search_ids_split[row[0]] == "valid" else "Private"

                solution_row = [row[0], row[7], relevance, usage]
                solution_writer.writerow(solution_row)
        i += len(nsmallest)
        print("%dk rows processed" % int(i/1000))
        if len(nsmallest)==batch_size:
            min_row = nsmallest[-1]
        else:
            rows_remaining = False
        f_raw.close()
        f_raw = open(raw_path)
        raw_reader = csv.reader(f_raw, delimiter="\t")
        header = raw_reader.next()
        reader = row_reader(ids_map, raw_reader) 

        f_train.flush()
        f_test.flush()
        f_solution.flush()
        f_position_benchmark.flush()

    f_raw.close()
    f_train.close()
    f_test.close()
    f_solution.close()
    f_position_benchmark.close()

if __name__=="__main__":
    np.random.seed(expedia_personalized_sort_data_split_seed())
    create_competition_data()