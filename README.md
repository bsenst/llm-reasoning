# Reasoning with the Help of Large Language Models

*This application is for experimental use only. It is not intended for real world use and does not replace medical advice.*

## Problem Statement

Clinical processes are speeding due to the growing workload. The ageing of societies results in more complex cases. Medical progress produces vast amounts of knowledge resulting in the need for specialization and subspecialization of medical professions. In everyday practice consulting patients with a plentitude of complaints gets more and more challenging.

## Solution 

As Technology advances in the field of Natural Language Processing collecting and analysing huge collections of data becomes more feasible. This offers chances to keep up with medical progress, consider complex patient cases and support reasoning at the point of care and just in time.

![architecture-llm-reasoning drawio (1)](https://github.com/bsenst/llm-reasoning/assets/8211411/50a88401-8225-4be8-a87d-29c625e11f4f)

This application serves an open source large language model Llama-2 that is connect to a streamlit user interface. The user can define a list of custom symptoms or ICD-10 symptoms as input to the LLM. A two-step chain of prompts will output a list of differential diagnoses followed by a list of examinations to workup these diagnoses. This experimental applications offers an impression on the perfomance of smaller LLM in diagnostic reasoning.

Videopresentation: https://youtu.be/kZszmwmItKA

## Next Steps

* Fine-tuning on public medical data not limited by security concerns.
* Fine-tuning on medical records when security can be preserved.
* Build additional modules beside differential diagnoses and proposals for diagnostic workup.
* Offer additional langchain integrations.
* Scaling to bigger large language models (i.e. Llama-2 70b).
* Connect to self-hosted LLM.

## Disclaimer

* A first version of this app has been developed and submitted as part of [lablab.ai & clarifai hackathon](https://lablab.ai/event/llama-2-hackathon-with-clarifai/fritzlab/llama-2-reasoning-support).
* The large language model is hosted on clarifai under the free community plan which might result in service limitation once the free requests are exceeded.

## Image Sources
* https://en.wikipedia.org/wiki/ICD-10#/media/File:Icd10codeslogo.png
* Company logos and products from the corresponding companies
