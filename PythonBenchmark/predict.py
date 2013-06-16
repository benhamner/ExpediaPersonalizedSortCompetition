import data_io

def main():
    print("Reading test data")
    train = data_io.read_test()
    features = []

    print("Loading the classifier")
    classifier = data_io.load_model()

    print("Making predictions")
    predictions = classifier.predict_proba(features)[:,1]
    predictions = list(predictions)

    print("Writing predictions to file")
    data_io.write_submission(predictions)

if __name__=="__main__":
    main()
