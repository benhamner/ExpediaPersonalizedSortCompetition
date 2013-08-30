import data_io
import numpy as np

def main():
    print("Reading test data")
    test = data_io.read_test()

    np.random.seed(1)
    ordinals = np.arange(len(test))
    np.random.shuffle(ordinals)

    recommendations = zip(test["srch_id"], test["prop_id"], ordinals)

    print("Writing predictions to file")
    data_io.write_submission(recommendations, "randomBenchmark.csv")

if __name__=="__main__":
    main()
