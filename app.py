import streamlit as st
from transformers import pipeline

# Page configuration
st.set_page_config(
    page_title="Fake News Detection",
    layout="centered"
)

# Custom CSS for clean layout
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

# Header
st.markdown("<h1>Fake News Detection</h1>", unsafe_allow_html=True)
st.write("This application predict whether a news article is real or fake.")

# Load model
@st.cache_resource
def load_model():
    MODEL = "jy46604790/Fake-News-Bert-Detect"
    return pipeline("text-classification", model=MODEL, tokenizer=MODEL)

classifier = load_model()

# Example inputs
examples = {
    "Select an example...": "",
    "Real News Example": (
        "NEW YORK & MAINZ, Germany--(BUSINESS WIRE)-- Pfizer Inc. (NYSE: PFE) and BioNTech SE (Nasdaq: BNTX) today announced "
        "updated data from a Phase 2/3 clinical trial demonstrating a robust neutralizing immune response one-month after a 30-µg "
        "booster dose of the companies’ Omicron BA.4/BA.5-adapted bivalent COVID-19 vaccine (Pfizer-BioNTech COVID-19 Vaccine, "
        "Bivalent (Original and Omicron BA.4/BA.5)). Immune responses against BA.4/BA.5 sublineages were substantially higher for "
        "those who received the bivalent vaccine compared to the companies’ original COVID-19 vaccine, with a similar safety and "
        "tolerability profile between both vaccines. These results reinforce the previously reported early clinical data measured 7 "
        "days after a booster dose of the bivalent vaccine, as well as the pre-clinical data, and suggest that a 30-µg booster dose of "
        "the Omicron BA.4/BA.5-adapted bivalent vaccine may induce a higher level of protection against the Omicron BA.4 and BA.5 "
        "sublineages than the original vaccine."
    ),
    "Fake News Example": (
        "NASA has confirmed that the Earth will experience six days of total darkness next month due to a rare planetary alignment. "
        "This once-in-a-lifetime event will reportedly block sunlight for nearly a week, plunging the world into complete darkness. "
        "Social media users are advised to stock up on supplies and stay indoors during this period. Scientists allegedly believe "
        "this phenomenon could also alter gravity, causing people to float temporarily."
    ),
}


# UI: Example selector
example_choice = st.selectbox("Choose an example to auto-fill the input field:", list(examples.keys()))
input_text = st.text_area(
    "Enter the news text below:",
    value=examples[example_choice],
    height=160,
    max_chars=3000
)

# Analyze button
if st.button("Analyze"):
    if not input_text.strip():
        st.warning("Please enter or select some news text.")
    else:
        with st.spinner("Analyzing..."):
            # Truncate to 500 words as per model limit
            truncated_text = " ".join(input_text.strip().split()[:500])
            result = classifier(truncated_text)[0]
            label = result["label"]
            score = result["score"]

        st.markdown("#### Prediction Result")
        if label == "LABEL_0":
            st.error(f"The text is likely **Fake News**. Confidence: {score:.2f}")
        elif label == "LABEL_1":
            st.success(f"The text is likely **Real News**. Confidence: {score:.2f}")
        else:
            st.warning(f"Unexpected label: {label}")


st.markdown("</div>", unsafe_allow_html=True)
