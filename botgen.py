import streamlit as st
import json
import os
import time


# Function to read JSON file
def read_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []


# Function to write to JSON file
def write_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


# Initialize JSON file name
json_file = "data/prompts.json"

# Title
st.title("BotGen")


# Create
with st.expander("Train Your Bot"):
    new_prompt = st.text_input("New Prompt")
    new_response = st.text_input("New Response")

    if st.button("Create"):
        new_data = {"prompt": new_prompt, "response": new_response}
        data = read_json(json_file)
        data.append(new_data)
        write_json(json_file, data)
        st.success("New data created")

# Read
with st.expander("Your Questions and Answers"):
    data = read_json(json_file)
    st.json(data)

# Update
with st.expander("Update Your Answers"):
    index_to_update = st.number_input(
        "Index to update", min_value=0, max_value=len(data) - 1, value=0
    )
    updated_prompt = st.text_input("Updated Prompt")
    updated_response = st.text_input("Updated Response")

    if st.button("Update"):
        data[index_to_update] = {"prompt": updated_prompt, "response": updated_response}
        write_json(json_file, data)
        st.success("Data updated")

# Delete
with st.expander("Delete Any Answers"):
    index_to_delete = st.number_input(
        "Index to delete", min_value=0, max_value=len(data) - 1, value=0
    )

    if st.button("Delete"):
        del data[index_to_delete]
        write_json(json_file, data)
        st.success("Data deleted")
# Train Chatbot Button
train_button_clicked = st.button("Train Your Chatbot")

# Progress Bar
progress_bar = st.empty()  # Placeholder for the progress bar

if train_button_clicked:
    progress_bar.progress(0)  # Start the progress bar at 0%

    for i in range(101):  # Simulating training progress
        progress_bar.progress(i)
        time.sleep(0.05)  # Simulating processing time
    progress_bar.empty()  # Clear the progress bar once training is done
    st.success("Chatbot training completed")
