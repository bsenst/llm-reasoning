import streamlit as st
from langchain.llms import Clarifai
from langchain import PromptTemplate, LLMChain

import uuid
import redis
from redis.commands.json.path import Path
from streamlit_feedback import streamlit_feedback

import os

# client = redis.Redis(host=st.secrets.REDIS_HOST, port=st.secrets.REDIS_PORT, db=st.secrets.REDIS_DB, password=st.secrets.REDIS_PASSWORD)
client = redis.Redis(host=os.environ.get("REDIS-HOST"), port=os.environ.get("REDIS-PORT"), db=os.environ.get("REDIS-DB"), password=os.environ.get("REDIS-PASSWORD"))

# Streamlit UI
st.title("Clinical Reasoning Support")
st.caption("This reasoning support does not replace clinical expertise. It is for experimental use only.")

model_id = st.selectbox("Select a large language model: ",
    ('llama2-7b-chat',
     'llama2-13b-chat'))

st.caption("Llama-2, an open-source LLM, published by Meta, provided by Clarifai https://clarifai.com/meta/Llama-2")

# https://python.langchain.com/docs/integrations/llms/clarifai
# clarifai_llm = Clarifai(
#     pat=st.secrets.PAT, user_id='meta', app_id='Llama-2', model_id=model_id, 
# )
clarifai_llm = Clarifai(
    pat=os.environ.get("PAT"), user_id='meta', app_id='Llama-2', model_id=model_id, 
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

if st.button("Generate List of Differential Diagnoses"):

    if selected_term:
        st.session_state["selected_term"] = selected_term
        differential_diagnoses = llm_chain.run(" ".join(selected_term))
        st.session_state["differential_diagnoses"] = differential_diagnoses
        diagnostic_workup = llm_chain2.run(differential_diagnoses)
        st.session_state["diagnostic_workup"] = diagnostic_workup
        
    else:
        st.write("Please select a single or several symptoms from the dropdown menu.")

if "selected_term" in st.session_state:
    st.write(f'Selected symptoms(s): {"; ".join(st.session_state["selected_term"])}')
    st.header("Differential Diagnoses")
    st.write(st.session_state["differential_diagnoses"])
    st.header("Diagnostic Workup")
    st.write(st.session_state["diagnostic_workup"])

if "selected_term" in st.session_state:

    st.session_state["feedback"] = streamlit_feedback(
        feedback_type="thumbs",
        align="flex-start",
    )

    st.caption("Give feedback to let us know what you think and report the symptoms, differential diagnoses and diagnostic workup.")

    if st.session_state["feedback"]:
        st.session_state["feedback"]["text"] = f'{st.session_state["selected_term"]}|{st.session_state["differential_diagnoses"]}|{st.session_state["diagnostic_workup"]}'
        client.json().set(f'user:{uuid.uuid4()}', '$', st.session_state["feedback"])
