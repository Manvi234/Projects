

## 💉 Onset of Diabetes Detection using Deep Learning

## ✅ Key Results: High-Performance Binary Classification

This project successfully developed a **Deep Neural Network (DNN)** model for predicting the onset of Type 2 Diabetes with high reliability on the PIMA Indians Diabetes Dataset.

| Metric | Result (%) | Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | **83.2%** | The overall percentage of correct predictions (diabetic and non-diabetic). |
| **F1-Score** | **77.0%** | The harmonic mean of precision and recall, demonstrating balanced performance. |
| **Precision** | **78.6%** | Of all positive (diabetic) predictions, 78.6% were correct (minimizing false positives). |
| **Recall** | **75.4%** | The model correctly identified 75.4% of all actual diabetic cases (minimizing false negatives). |

---

## 🎯 Project Goal & Methodology

The primary goal was to create a robust and highly accurate model capable of predicting the onset of diabetes based on patient diagnostic data.

| Area | Approach |
| :--- | :--- |
| **Model Type** | **Deep Neural Network (DNN)** / Multi-Layer Perceptron (MLP) |
| **Problem Type** | Binary Classification (Diabetic vs. Non-Diabetic) |
| **Objective** | Maximize **Accuracy** and **F1-Score** while maintaining high **Recall** (to minimize missed diagnoses). |

### Dataset & Features

The model was trained on the PIMA Indians Diabetes Dataset. Features include standard diagnostic measurements:

* **Key Features:** `Glucose`, `BMI`, `Age`, `BloodPressure`, `Insulin`, `DiabetesPedigreeFunction`.
* **Target Variable:** `Outcome` (**1 = Diabetic**, **0 = Non-Diabetic**).

---

## ⚙️ Model Design & Analysis

The deep learning solution employs multiple dense layers to learn complex, non-linear relationships within the patient data.

### 1. Data Preprocessing
* **Data Cleaning:** Handled zero values in diagnostic fields (`BloodPressure`, `BMI`, etc.) which often represent missing data in this specific dataset.
* **Scaling:** All numerical features were normalized using **`StandardScaler`** to ensure equal weight during training, which is critical for DNN stability.

### 2. Deep Neural Network Architecture
The network uses a sequential model with multiple Dense layers built with **Keras/TensorFlow**:

* **Activation Functions:** **ReLU** in the hidden layers for non-linearity, and **Sigmoid** in the output layer to provide the final probability score (0 to 1).
* **Optimization:** The **Adam** optimizer was used with **Binary Cross-Entropy** as the loss function.

---

## 🛠️ Technology Stack

| Category | Tools/Libraries |
| :--- | :--- |
| **Language** | Python |
| **Deep Learning** | **TensorFlow / Keras** |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (Preprocessing, Model Evaluation) |
| **Visualization** | Matplotlib, Seaborn |
