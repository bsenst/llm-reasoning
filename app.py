import streamlit as st
from langchain.llms import Clarifai
from langchain import PromptTemplate, LLMChain

# Streamlit UI
st.title("Clinical Reasoning Support")
st.caption("This reasoning support does not replace clinical expertise. It is for experimental use only.")

model_id = st.selectbox("Select a large language model: ",
    ('llama2-13b-chat',
    'llama2-7b-chat'))

# https://python.langchain.com/docs/integrations/llms/clarifai
clarifai_llm = Clarifai(
    pat=st.secrets.PAT, user_id='meta', app_id='Llama-2', model_id=model_id, 
)

template = """Symptom or list of symptoms: {symptom}

These symptoms can be caused by the following list of diseases: """

prompt = PromptTemplate(template=template, input_variables=["symptom"])

# Create LLM chain
llm_chain = LLMChain(prompt=prompt, llm=clarifai_llm)

template2 = """List of differential diagnoses: {differential_diagnoses}

For this list of differential diagnoses the following list of diagnostic method is necessary for workup: """

prompt2 = PromptTemplate(template=template2, input_variables=["differential_diagnoses"])

# Create LLM chain
llm_chain2 = LLMChain(prompt=prompt2, llm=clarifai_llm)


# Create a list of specified terms for the dropdown menu
with open("icd10_symptoms.txt") as infile:
    icd_terms = infile.read().split("\n")

# Dropdown menu for selecting a term
selected_icd = st.multiselect("Choose one or more ICD symptom codes:", icd_terms)

st.caption("The processed list of symptoms originally comes from https://github.com/bryand1/icd10-cm under MIT-License.")

# Create a list of specified terms for the dropdown menu
with open("symptoms.txt") as infile:
    selected_terms = infile.read().split("\n")

# Dropdown menu for selecting a term
selected_term = st.multiselect("Choose one or more symptom(s):", selected_terms)

selected_term = selected_term + selected_icd

def clean_output(output):
    cleaned_output = []
    for line in [line for line in output.split("\n") if line!=""]:
        if "." in line:
            if line.split(".")[0][-1].isnumeric():
                cleaned_output.append(line)
            else:
                break
    return "\n".join(cleaned_output)

# Button to generate output
if st.button("Generate List of Differential Diagnoses"):
    if selected_term:
        st.write(f"Selected symptoms(s): {'; '.join(selected_term)}")
        differential_diagnoses = llm_chain.run(" ".join(selected_term))
        differential_diagnoses = clean_output(differential_diagnoses)
        st.header("Differential Diagnoses")
        st.write(differential_diagnoses)
        st.header("Diagnostic Workup")
        diagnostic_workup = llm_chain2.run(differential_diagnoses)
        st.write(diagnostic_workup)

    else:
        st.write("Please select a single or several symptoms from the dropdown menu.")
