import streamlit as st
from langchain.llms import Clarifai
from langchain import PromptTemplate, LLMChain

# https://python.langchain.com/docs/integrations/llms/clarifai
clarifai_llm = Clarifai(
    pat=st.secrets.PAT, user_id='meta', app_id='Llama-2', model_id='llama2-13b-chat'
)

template = """Symptom or list of symptoms: {symptom}

These symptoms can be caused by the following diseases: """

prompt = PromptTemplate(template=template, input_variables=["symptom"])

# Create LLM chain
llm_chain = LLMChain(prompt=prompt, llm=clarifai_llm)

# Create a list of specified terms for the dropdown menu
with open("symptoms.txt") as infile:
    specified_terms = infile.read().split("\n")

# Streamlit UI
st.title("Llama-2 Reasoning Support")

# Dropdown menu for selecting a term
selected_term = st.multiselect("Select a term(s):", specified_terms)

# Button to generate output
if st.button("Generate Output"):
    if selected_term:
        st.write(f"Selected symptoms(s): {', '.join(selected_term)}")
        st.write(llm_chain.run(" ".join(selected_term)))
    else:
        st.write("Please select a single or several symptoms from the dropdown menu.")

st.caption("This reasoning support does not replace clinical expertise. It is only for experimental use.")
