import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4
INT_VARIABLES = (0, 2, 4, 11, 12, 13, 14)
FLOAT_VARIABLES = (1, 3, 5, 6, 7, 8, 9)
MONTH = 10
VISITOR_TYPE = 15
WEEKEND = 16
REVENUE = 17


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


def month(month_abbr):
    return {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'June': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11,
    }[month_abbr]


def visitor_type(visitor):
    return {
        'New_Visitor': 0,
        'Returning_Visitor': 1,
        'Other': 0
    }[visitor]


def weekend(weekday):
    return {
        'TRUE': 1,
        'FALSE': 0
    }[weekday]


def revenue(buy):
    return {
        'TRUE': 1,
        'FALSE': 0
    }[buy]


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Create evidence list
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        evidence = []
        for row in reader:
            evidence.append(
                [cell for cell in row[:17]]
            )

    # Create label list
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        label = []
        for row in reader:
            label.append(
                revenue(row[17])
            )

    # Iterate over evidence list and cast variables as required types
    evidence_length = len(evidence)
    row_length = len(evidence[0])

    for i in range(evidence_length):
        for j in range(row_length):
            if j in INT_VARIABLES:
                evidence[i][j] = int(evidence[i][j])
            elif j in FLOAT_VARIABLES:
                evidence[i][j] = float(evidence[i][j])
            elif j == MONTH:
                evidence[i][j] = month(evidence[i][j])
            elif j == VISITOR_TYPE:
                evidence[i][j] = visitor_type(evidence[i][j])
            elif j == WEEKEND:
                evidence[i][j] = weekend(evidence[i][j])

    # Return two evidence and label as a tuple
    return_tuple = (evidence, label)

    return return_tuple


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neighbors_classifier = KNeighborsClassifier(n_neighbors=1)
    neighbors_classifier.fit(evidence, labels)
    return neighbors_classifier


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

    true_positive = 0
    true_negative = 0
    all_positives = 0
    all_negatives = 0

    for label, prediction in zip(labels, predictions):
        if label == 1:
            all_positives += 1
        if label == prediction and label == 1:
            true_positive += 1
        if label == 0:
            all_negatives += 1
        if label == prediction and label == 0:
            true_negative += 1

    sensitivity = true_positive / all_positives
    specificity = true_negative / all_negatives

    return sensitivity, specificity


if __name__ == "__main__":
    main()
