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

st.markdown('This free open source app was initially built during [IOOS Code Sprint 2022](https://ioos.github.io/ioos-code-sprint/topics/07-ioos-qc-non-programmers/).')

st.markdown('If you wish to run the code locally or contribute to this app, please check out our repository: [ioos qc front end](https://github.com/Dylan-Pugh/ioos-qc-front-end).')

st.markdown('If you have any questions or comments on this app, please submit them [here as a new issue](https://github.com/Dylan-Pugh/ioos-qc-front-end/issues).')

st.markdown('[Example Water Level Test File](https://github.com/Dylan-Pugh/ioos-qc-front-end/raw/main/water_level_example_test.csv)')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
     # Can be used wherever a "file-like" object is accepted:
     df = pd.read_csv(uploaded_file)

     with st.expander(label='Dataset Preview', expanded=True):
        st.write(df.head())
    
     st.markdown('Select **sea_surface_height_above_sea_level** if you are using Example Water Level Test File')
    
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
                 col1, col2 = st.columns([1,1])
                 with col1:
                     lower_bound = st.number_input(label='Override Lower Bound', value=min(test_config[current_param]))
                 with col2:
                     upper_bound = st.number_input(label='Override Upper Bound', value=max(test_config[current_param]))
                 range = [upper_bound, lower_bound]

                 values = st.slider(label=current_param, value=range)
                 #st.write(values)
                 config['qartod'][selected_test][current_param] = values
                 #st.write(config)
    
     if st.button(label='Run Tests'):
         write_config(config)
         result = run_test.run_tests(df, selected_column, config)
    
         if not result.empty:
            st.success('Processing successful.')
            results_csv = convert_df(result)

            st.download_button(
                label="Download data as CSV",
                data=results_csv,
                file_name='results.csv',
                mime='text/csv',
            )
