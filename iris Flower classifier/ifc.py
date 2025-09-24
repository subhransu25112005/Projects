# ------------------------------
# Iris Flower Classifier Project
# ------------------------------

# Import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. Load Dataset
iris = load_iris()
X = iris.data       # Features: sepal & petal measurements
y = iris.target     # Labels: species

# Convert to DataFrame for better visualization
df = pd.DataFrame(X, columns=iris.feature_names)
df['species'] = [iris.target_names[i] for i in y]

print("Sample Data:")
print(df.head())

# 2. Visualize Data
sns.pairplot(df, hue="species", palette="deep")
plt.show()

# 3. Split into Train & Test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 5. Train Model (KNN)
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# 6. Predictions
y_pred = model.predict(X_test)

# 7. Evaluation
print("\nModel Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=iris.target_names))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 8. Test with Custom Input
sample = np.array([[5.1, 3.5, 1.4, 0.2]])  # Example measurement
sample_scaled = scaler.transform(sample)
prediction = model.predict(sample_scaled)
print("\nCustom Prediction:", iris.target_names[prediction[0]])