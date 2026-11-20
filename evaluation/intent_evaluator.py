
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support
)

# Project root
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.router import detect_intent, Intent


# All supported intent classes
LABELS = [
    "QUESTION_LOOKUP",
    "CODE_FIX",
    "HINT_REQUEST",
    "CONCEPT_QUESTION",
    "GENERAL_CHAT",
    "SOLUTION_REQUEST",
]

DATASET_PATH = ROOT / "evaluation" / "datasets" / "intent_test.csv"
RESULTS_DIR = ROOT / "evaluation" / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def evaluate_intent_router():

    print("\n===== SahiiiDSA Intent Router Evaluation =====\n")

    # Load dataset
    df = pd.read_csv(DATASET_PATH)

    required_columns = {
        "message",
        "expected_intent",
        "has_code_block"
    }

    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Dataset must contain columns: {required_columns}"
        )

    if df.empty:
        raise ValueError("The test dataset is empty.")

    if not df["expected_intent"].isin(LABELS).all():
        raise ValueError("Dataset contains an unknown intent label.")

    y_true = []
    y_pred = []

    # Run actual project router
    for index, row in df.iterrows():

        message = str(row["message"])

        has_code = str(row["has_code_block"]).strip().lower() == "true"

        expected = row["expected_intent"]

        predicted = detect_intent(
            message,
            has_code_block=has_code
        ).name

        y_true.append(expected)
        y_pred.append(predicted)

        status = "PASS" if expected == predicted else "WRONG"

        print(f"\nTest {index + 1}: {status}")
        print(f"Message   : {message}")
        print(f"Expected  : {expected}")
        print(f"Predicted : {predicted}")

    # Overall accuracy
    accuracy = accuracy_score(y_true, y_pred)

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            y_true,
            y_pred,
            labels=LABELS,
            average="macro",
            zero_division=0
        )
    )

    print("\n===== Overall Metrics =====")
    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"Macro F1  : {f1:.4f}")

    # Detailed classification report
    report = classification_report(
        y_true,
        y_pred,
        labels=LABELS,
        output_dict=True,
        zero_division=0
    )

    report_df = pd.DataFrame(report).transpose()

    report_path = RESULTS_DIR / "classification_report.csv"
    report_df.to_csv(report_path)

    print("\n===== Classification Report =====")
    print(classification_report(
        y_true,
        y_pred,
        labels=LABELS,
        zero_division=0
    ))

    # Save individual predictions
    predictions = df.copy()
    predictions["predicted_intent"] = y_pred
    predictions["correct"] = [
        actual == predicted
        for actual, predicted in zip(y_true, y_pred)
    ]

    predictions.to_csv(
        RESULTS_DIR / "predictions.csv",
        index=False
    )

    # Confusion matrix
    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=LABELS
    )

    plt.figure(figsize=(11, 8))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=LABELS,
        yticklabels=LABELS
    )

    plt.title("SahiiiDSA - Intent Router Confusion Matrix")
    plt.xlabel("Predicted Intent")
    plt.ylabel("Actual Intent")
    plt.xticks(rotation=35, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    matrix_path = RESULTS_DIR / "confusion_matrix.png"
    plt.savefig(matrix_path, dpi=300)
    plt.close()

    print("\n===== Evaluation Completed =====")
    print(f"Confusion Matrix : {matrix_path}")
    print(f"Classification Report : {report_path}")
    print(f"Predictions : {RESULTS_DIR / 'predictions.csv'}")


if __name__ == "__main__":
    evaluate_intent_router()
