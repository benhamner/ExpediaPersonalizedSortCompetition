import data_io

def main():
    print("Reading test data")
    test = data_io.read_test()
    test.fillna(0, inplace=True)
    
    feature_names = list(test.columns)
    feature_names.remove("date_time")

    features = test[feature_names].values

    print("Loading the classifier")
    classifier = data_io.load_model()

    print("Making predictions")
    predictions = classifier.predict_proba(features)[:,1]
    predictions = list(-1.0*predictions)
    recommendations = zip(test["srch_id"], test["prop_id"], predictions)

    print("Writing predictions to file")
    data_io.write_submission(recommendations)

if __name__=="__main__":
    main()
