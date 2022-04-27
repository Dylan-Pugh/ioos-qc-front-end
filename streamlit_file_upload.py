import streamlit as st
import pandas as pd
import json
import run_test

config_file_path = "qc_config.json"

def write_config(config_to_write):
    with open (config_file_path, 'w') as out_file:
        json.dump(config_to_write, out_file)

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

st.title("IOOS QC Web Application")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
     # Can be used wherever a "file-like" object is accepted:
     df = pd.read_csv(uploaded_file)

     with st.expander(label='Dataset Preview', expanded=True):
        st.write(df.head())
    
     selected_column = st.selectbox(label='Select Input Variable', options=df.columns)

     # Load QC config
     with open (config_file_path) as config_json:
        config = json.load(config_json)

     selected_test = st.selectbox(label='Select QC Test', options=config['qartod'].keys())

     # Display options for selected test

     test_config = config['qartod'][selected_test]
     test_label = 'Configure Test: ' + selected_test
     #st.write(test_config)

     with st.expander(label=test_label, expanded=True):
         for current_param in test_config.keys():
             if isinstance(test_config[current_param], list):
                 values = st.slider(label=current_param, value=test_config[current_param])
                 #st.write(values)
                 config['qartod'][selected_test][current_param] = values
                 #st.write(config)
    
     if st.button(label='Run Tests'):
         write_config(config)
         result = run_test.run_tests(df, selected_column, config)
    
         if not result.empty:
            results_csv = convert_df(result)

            st.download_button(
                label="Download data as CSV",
                data=results_csv,
                file_name='results.csv',
                mime='text/csv',
            )