

## 🧠 Classification of Cognitive Distortions in CBT Text

## 🏆 Key Results: High-Accuracy Imbalanced Classification

This project investigated the optimal combination of data balancing, feature selection, and classification algorithms for identifying cognitive distortions in patient-therapist interactions. The final model achieved near-perfect performance.
|Feature Selection| Classifier| Data Balancing| F1-Score |
| :--- | :--- | :--- | :--- |
|TF-IDF| SVC| SMOTE-Tomek| 0.99 (optimal) |
|TF-IDF|Random Forest|SMOTE-Tomek|0.97 |
|spaCy|Random Forest|SMOTE-Tomek|0.972 |

---

## 🎯 Project Goal & Methodology

The goal was to integrate Machine Learning and NLP techniques into Cognitive Behavioral Therapy (CBT) systems to **automatically detect and classify cognitive distortions** (negative thinking patterns) from patient text.

| Area | Approach |
| :--- | :--- |
| **Problem Type** | Multi-Class Text Classification |
| **Input Data** | Annotated patient-therapist interaction text (Patient Questions) |
| **Challenge** | **Severe data imbalance** (majority class: "No Distortion") |
| **Objective** | Achieve high **F1-Score** and **Accuracy** on all distortion classes. |

### Cognitive Distortions Detected

The model was trained to classify **eleven unique categories** of cognitive distortions, including:

* **All-or-nothing thinking** (Black-and-White Thinking)
* **Overgeneralization**
* **Mental filter** (Selective Attention)
* **Should statements**
* **Personalization**
* **Mind Reading**
* **Emotional Reasoning**

---

## ⚙️ Technical Pipeline & Analysis

The proposed system follows a structured pipeline of preprocessing, data balancing, feature selection, and ensemble modeling.



### 1. Data Preprocessing (NLP)

The raw text data was cleaned and standardized using the NLTK library:

* Conversion to lowercase and elimination of white spaces.
* Punctuation and **Stop Word** removal (common filler words).
* **Tokenization** (splitting sentences into words).
* **Lemmatization** using WordNetLemmatizer (reducing words to their base form).

### 2. Hybrid Data Balancing (SMOTE-Tomek)

The visualization of the dataset confirmed a **severe class imbalance**, where the "No Distortion" class vastly outnumbered all specific distortion types (as shown in Fig. 2). This requires specific attention as standard classifiers would be biased toward the majority class.

* **Method:** **SMOTE-Tomek** was applied to balance the dataset.
* **Mechanism:** This hybrid approach uses **SMOTE (Synthetic Minority Over-sampling Technique)** to generate new synthetic samples for the minority classes, followed by **Tomek Links** undersampling to remove noisy and overlapping instances, particularly from the majority class boundary. This combination enhances the separation between classes.

### 3. Feature Selection & Vectorization

Two methods were tested to convert text into numerical vectors that machine learning algorithms can process:

* **TF-IDF (Term Frequency-Inverse Document Frequency):** Measures how important a word is to a document in a collection.
* **spaCy:** Uses pre-trained language models for vectorization.

| Feature Selection Method | **Performance Insight** |
| :--- | :--- |
| **TF-IDF** | Consistently **outperformed** spaCy under both balanced and unbalanced conditions. |
| **spaCy** | Showed lower overall scores, particularly in the F1-Score, indicating poorer handling of minority classes. |

### 4. Classifier Performance

Ensemble methods **Random Forest (RF)**, **XGBoost**, and **Support Vector Classifier (SVC)** consistently outperformed individual classifiers.

| Algorithm | TF-IDF w/ SMOTE-Tomek (F1-Score) | spaCy w/ SMOTE-Tomek (F1-Score) |
| :--- | :--- | :--- |
| **Support Vector Classifier (SVC)** | **0.99** | 0.64 |
| **Random Forest Classifier** | 0.97 | 0.972 |
| **XGBoost** | 0.93 | 0.971 |
| **Decision Tree** | 0.82 | 0.71 |
| *Gaussian NB* | 0.96 | 0.32 |

The **Support Vector Classifier (SVC)** achieved the highest F1-Score of **0.99** when paired with **TF-IDF** and **SMOTE-Tomek**. The close alignment between Accuracy (99%) and F1-Score (0.99) confirms that the model is predicting the minority classes just as effectively as the majority class—a crucial success for an imbalanced classification problem.

---

## 🛠️ Technology Stack & Future Scope

| Category | Tools/Libraries |
| :--- | :--- |
| **Language** | Python |
| **ML Framework** | **Scikit-learn** (Classifiers, Metrics) |
| **NLP** | **NLTK, spaCy** |
| **Vectorization** | **TF-IDF** |
| **Ensemble** | **XGBoost, Random Forest, AdaBoost** |
| **Data Imbalance** | **SMOTE-Tomek** |

### Future Scope

The project suggests expanding the research into **Deep Learning models** using **multimodal data** (audio and video inputs) to capture nonverbal cues, emotional states, intonations, and pitch variations. This integration would enhance the adaptability and personalization of CBT systems by providing a more comprehensive picture of a user’s emotional well-being.
