import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


# ==========================
# Load Dataset
# ==========================

df = pd.read_csv(r"app\ml\diabetes.csv")

print(df.head())
print(df.columns)


# ==========================
# Features & Target
# ==========================

X = df.drop("Outcome", axis=1)
y = df["Outcome"]


# ==========================
# Train Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==========================
# Scaling
# ==========================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# ==========================
# Models
# ==========================

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42
    ),

    "KNN": KNeighborsClassifier(
        n_neighbors=7
    ),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=5,
        random_state=42
    )
}


# ==========================
# Compare Models
# ==========================

best_model = None
best_accuracy = 0
best_model_name = ""

for name, model in models.items():

    model.fit(
        X_train,
        y_train
    )

    y_pred = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    print(
        f"Accuracy: {accuracy:.4f}"
    )

    print(
        classification_report(
            y_test,
            y_pred
        )
    )

    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_model_name = name


# ==========================
# Save Best Model
# ==========================

with open(
    "app/ml/model.pkl",
    "wb"
) as f:

    pickle.dump(
        best_model,
        f
    )

with open(
    "app/ml/scaler.pkl",
    "wb"
) as f:

    pickle.dump(
        scaler,
        f
    )


# ==========================
# Final Result
# ==========================

print("\n" + "=" * 50)
print("BEST MODEL")
print("=" * 50)

print(
    f"Model: {best_model_name}"
)

print(
    f"Accuracy: {best_accuracy:.4f}"
)

print(
    "\nBest model saved successfully!"
)