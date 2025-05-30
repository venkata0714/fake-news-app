
---

## 📰 Fake News Detection Web App

This is a lightweight, production-ready web application built with **Streamlit** for classifying news articles as **Fake** or **Real** using a traditional machine learning model trained on TF-IDF features.

---

### 🚀 Features

* 🧠 **Pretrained ML model** using `scikit-learn` and `TfidfVectorizer`
* 🧹 **NLTK-based preprocessing** with stemming and stopword removal
* 🧪 Interactive **web interface** with example inputs
* ✅ Supports long-form article inputs (up to 3000 characters)
* ⚡ Fast predictions without needing transformers or GPU

---

### 🧰 Technologies Used

* Python 3.8+
* Streamlit
* scikit-learn
* NLTK
* Joblib

---

### 📂 Project Structure

```
.
├── app.py               # Main Streamlit app
├── model.pkl            # Trained classification model (e.g., LogisticRegression)
├── tfidfvect.pkl        # Trained TfidfVectorizer
├── requirements.txt     # Dependencies
├── nltk_data/           # Optional NLTK data folder (stopwords)
└── README.md
```

---
