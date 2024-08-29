'''
pip install langchain_core langchain_groq python-dotenv ctransformers sentence-transformers pinecone-client langchain langchain-community langchain_pinecone pypdf
'''

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file

import os
from langchain.chains import LLMChain
from langchain_groq.chat_models import ChatGroq
import pandas as pd
from langchain.chains  import RetrievalQA

key = "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"

######################################### Appointment Code ##############################
def chat_model(temperature):
    return ChatGroq(
        temperature=temperature,
        model_name="llama3-70b-8192",  # Larger model for complex healthcare info
        api_key=key,

    )

# Filepaths to data
doctors_csv_path = "DATA/doctors_data.csv"
appointments_csv_path = "DATA/appointments.csv"
df_doctors = pd.read_csv(doctors_csv_path)
from langchain.chains import LLMChain



prompt_classify = PromptTemplate(
    input_variables=["query"],
    template="""
    You are a medical assistant. Your task is to classify the following
    query into medical specializations such as:
    - Dermatologist
    - Cardiologist
    - Ophthalmologist
    - Neurologist
    - Radiologist
    and so on
    Return only the
    Specialization:

    Query: {query}
    """
)


llm = chat_model(0.5)
chain = LLMChain(llm=llm, prompt=prompt_classify)


def classify_query(query):
    specialization = chain.run({"query": query}).strip()
    #returns only specialization
    return specialization

# Function to search for available doctors in the csv based on location, specialization and availability
def search_doctors(location, specialization):
    available_doctors = df_doctors[(df_doctors['Location'] == location) &
                                   (df_doctors['Specialization'] == specialization) &
                                   (df_doctors['Availability'] == 'YES')]
    return available_doctors


import os
location = "Karachi"
# for booking appointments, appointments are stored in appointment.csv
def book_appointment(doctor_id, user_name, user_query, appointments_csv_path):
    appointment = {
        "Doctor_id": doctor_id,
        "User_name": user_name,
        "Query": user_query,
        "Status": "Booked"
    }

    # Check if the appointments CSV file exists; if not, create a new
    if os.path.exists(appointments_csv_path):
        df_appointments = pd.read_csv(appointments_csv_path)
    else:
        df_appointments = pd.DataFrame(columns=["Doctor_id", "User_name", "Query", "Status"])

    # Append the new appointment to the DataFrame
    df_appointments = pd.concat([df_appointments, pd.DataFrame([appointment])], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df_appointments.to_csv(appointments_csv_path, index=False)
    
input_text = "I have brain stroke, please help"
### Main Code that connects all
def medical_bot(user_name, user_query, user_location):
    specialization = classify_query(user_query)
    available_doctors = search_doctors(user_location, specialization)

    if not available_doctors.empty:
        doctor = available_doctors.iloc[0]
        print(f"Found a doctor: {doctor['Name']} ({doctor['Specialization']}) in {user_location}.")
        print("Do you want to book an appointment with this doctor?")

        # Assuming user input for confirmation UI part
        user_response = input("Enter 'yes' to book or 'no' to decline: ").lower().strip()

        if user_response == 'yes' or 'y':
            # appointments_csv_path 
            book_appointment(doctor['Doctor_id'], user_name, user_query, appointments_csv_path)
            confirmation_message = f"Appointment booked with {doctor['Name']} ({doctor['Specialization']}) in {user_location}."
            print(confirmation_message)
            return confirmation_message
        else:
            return "Appointment not booked."
    else:
        return "Good Luck"
####################################### Finished ###################################
medical_bot(user_name="XYZ", user_query=input_text, user_location=location) #location will be provided by API

