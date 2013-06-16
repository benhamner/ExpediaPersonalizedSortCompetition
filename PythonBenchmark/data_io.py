import csv
import os
import json
import pickle
import pandas as pd

def get_paths():
    paths = json.loads(open("SETTINGS.json").read())
    for key in paths:
        paths[key] = os.path.expandvars(paths[key])
    return paths

def read_train():
    train_path = get_paths()["train_path"]
    return pd.read_csv(train_path)

def read_test():
    test_path = get_paths()["test_path"]
    return pd.read_csv(test_path)

def save_model(model):
    out_path = get_paths()["model_path"]
    pickle.dump(model, open(out_path, "w"))

def load_model():
    in_path = get_paths()["model_path"]
    return pickle.load(open(in_path))

def write_submission(predictions):
    submission_path = get_paths()["submission_path"]
    rows = [(author_id, paper_ids_to_string(predictions[author_id])) for author_id in predictions]
    writer = csv.writer(open(submission_path, "w"), lineterminator="\n")
    writer.writerow(("AuthorId", "PaperIds"))
    writer.writerows(rows)
