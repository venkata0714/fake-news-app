import streamlit as st
import joblib
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Setup
ps = PorterStemmer()
nltk.data.path.append('./nltk_data')
nltk.download('stopwords', download_dir='./nltk_data')

# Page config
st.set_page_config(page_title="Fake News Detection", layout="centered")

# Load model/vectorizer
@st.cache_resource
def load_model_and_vectorizer():
    model = joblib.load("model.pkl")
    tfidfvect = joblib.load("tfidfvect.pkl")
    return model, tfidfvect

model, tfidfvect = load_model_and_vectorizer()

# Define prediction class
class PredictionModel:
    def __init__(self, original_text):
        self.output = {'original': original_text}

    def preprocess(self):
        review = re.sub('[^a-zA-Z]', ' ', self.output['original'])
        review = review.lower().split()
        review = [ps.stem(word) for word in review if word not in stopwords.words('english')]
        cleaned_text = ' '.join(review)
        self.output['preprocessed'] = cleaned_text
        return cleaned_text

    def predict(self):
        review = self.preprocess()
        text_vect = tfidfvect.transform([review]).toarray()
        prediction = model.predict(text_vect)[0]
        self.output['prediction'] = 'FAKE' if prediction == 0 else 'REAL'
        return self.output

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.05);
        }
        h1 {
            font-size: 2rem;
            font-weight: 600;
            color: #333333;
        }
        .stTextArea textarea {
            font-size: 16px;
            padding: 10px;
        }
        .stButton>button {
            font-size: 16px;
            padding: 0.5rem 1.5rem;
            background-color: #0d6efd;
            color: white;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

# UI Layout
st.markdown("<h1>Fake News Detection</h1>", unsafe_allow_html=True)
st.write("This application predicts whether a news article is real or fake using a traditional ML model.")

examples = {
    "Select an example...": "",
    "Real News Example": (
        "NEW YORK & MAINZ, Germany--(BUSINESS WIRE)-- Pfizer Inc. (NYSE: PFE) and BioNTech SE (Nasdaq: BNTX) today announced "
        "updated data from a Phase 2/3 clinical trial demonstrating a robust neutralizing immune response one-month after a 30-µg "
        "booster dose of the companies’ Omicron BA.4/BA.5-adapted bivalent COVID-19 vaccine (Pfizer-BioNTech COVID-19 Vaccine, "
        "Bivalent (Original and Omicron BA.4/BA.5)). Immune responses against BA.4/BA.5 sublineages were substantially higher for "
        "those who received the bivalent vaccine compared to the companies’ original COVID-19 vaccine, with a similar safety and "
        "tolerability profile between both vaccines..."
    ),
    "Fake News Example": (
        "NASA has confirmed that the Earth will experience six days of total darkness next month due to a rare planetary alignment. "
        "This once-in-a-lifetime event will reportedly block sunlight for nearly a week, plunging the world into complete darkness. "
        "Social media users are advised to stock up on supplies and stay indoors during this period. Scientists allegedly believe "
        "this phenomenon could also alter gravity, causing people to float temporarily."
    ),
}


example_choice = st.selectbox("Choose an example to auto-fill:", list(examples.keys()))
input_text = st.text_area("Enter the news article text below:", value=examples[example_choice], height=160)

if st.button("Analyze"):
    if not input_text.strip():
        st.warning("Please enter:")
    else:
        with st.spinner("Analyzing..."):
            predictor = PredictionModel(input_text)
            result = predictor.predict()
        st.markdown("#### Prediction Result")
        if result["prediction"] == "FAKE":
            st.error(f"The text is likely **Fake News**.")
        else:
            st.success(f"The text is likely **Real News**.")
        st.markdown("##### Preprocessed Text")
        st.code(result["preprocessed"])
