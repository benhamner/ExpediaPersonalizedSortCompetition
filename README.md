Expedia Personalized Sort Competition
=====================================

This repo contains a benchmark and sample code in Python for the [Expedia Personalized Sort Competition](https://www.kaggle.com/c/expedia-personalized-sort), a machine learning challenged hosted by [Kaggle](https://www.kaggle.com) in conjunction with [Expedia](http://www.expedia.com/).

It also contains the transformation code used to create the competition data files from the raw data in the CreateCompetitionData directory. This code is provided for your information only (and does not need to be looked at or run by competition participants).

This version of the repo contains the **Basic Python Benchmark**. Future benchmarks may be included here as well and will be marked with git tags.

This benchmark is intended to provide a simple example of reading the data and creating the submission file, not as a state of the art benchmark on this problem.

Executing this benchmark requires Python 2.7, along with the Python package sklearn version 0.13, and pandas version 0.10.1 (other versions may work, but this has not been tested).

To run the benchmark,

1. [Download data.zip from the competition page](https://www.kaggle.com/c/expedia-personalized-sort/data). This contains the dataset as two csv files, train.csv and test.csv.
3. Switch to the "PythonBenchmark" directory
4. Modify SETTINGS.json to include the paths to the data files, as well as a place to save the trained model and a place to save the submission
5. Train the model by running `python train.py`
6. Make predictions on the validation set by running `python predict.py`
7. [Make a submission](https://www.kaggle.com/c/expedia-personalized-sort/team/select) with the output file

This benchmark took less than 5 minutes to execute on a Windows 8 laptop with 8GB of RAM and 4 cores at 2.7GHz.