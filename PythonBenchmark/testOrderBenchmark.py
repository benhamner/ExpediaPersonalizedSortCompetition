import data_io
import numpy as np

def main():
    print("Reading test data")
    test = data_io.read_test()

    ordinals = np.arange(len(test))

    recommendations = zip(test["srch_id"], test["prop_id"], ordinals)

    print("Writing predictions to file")
    data_io.write_submission(recommendations, "testOrderBenchmark.csv")

if __name__=="__main__":
    main()
