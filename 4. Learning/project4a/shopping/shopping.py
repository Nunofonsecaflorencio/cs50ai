import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        0 - Administrative, an integer
        1 - Administrative_Duration, a floating point number
        2 - Informational, an integer
        3 - Informational_Duration, a floating point number
        4 - ProductRelated, an integer
        5 - ProductRelated_Duration, a floating point number
        6 - BounceRates, a floating point number
        7 - ExitRates, a floating point number
        8 - PageValues, a floating point number
        9 - SpecialDay, a floating point number
        10 - Month, an index from 0 (January) to 11 (December)
        11 - OperatingSystems, an integer
        12 - Browser, an integer
        13 - Region, an integer
        14 - TrafficType, an integer
        15 - VisitorType, an integer 0 (not returning) or 1 (returning)
        16- Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    def parse(index, value):
        if index in [0, 2, 4, 11, 12, 13, 14]:
            return int(value)
        
        if index in [1, 3, 5, 6, 7, 8, 9]:
            return float(value)
        
        if index == 10:
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            return months.index(value)
        
        if index == 15:
            return 1 if value == "Returning_Visitor" else 0
        
        if index in [16, 17]:
            return 1 if value == "TRUE" else 0
        
        return value
    
    
    evidence = list()
    labels = list()
    
    with open(filename) as file:
        reader = csv.reader(file)
        
        next(reader)
        for row in reader:
            row_len = len(row)
            
            evidence.append(
                [parse(index, value) for index, value in enumerate(row[:row_len - 1])]
            )
        
            labels.append(parse(row_len - 1, row[row_len - 1]))
            
        
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """ 
    true_positives = true_negatives = 0.0
    false_positives = false_negatives = 0.0
    
    for label, prediction in zip(labels, predictions):
        
        if prediction == 1:         # _positives
            if label == prediction:
                true_positives += 1
            else:
                false_positives += 1
        else:                       # _negatives
            if label == prediction:
                true_negatives += 1
            else:
                false_negatives += 1           
                     
    sensitivity = true_positives / (true_positives + false_negatives)
    specificity = true_negatives / (true_negatives + false_positives)
    
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
