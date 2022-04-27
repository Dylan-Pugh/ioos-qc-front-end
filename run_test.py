import pandas as pd
import numpy as np
from datetime import datetime
from ioos_qc.config import QcConfig
from ioos_qc import qartod

# Water level data
# For a fixed station in Kotzebue, AK (https://www.google.com/maps?q=66.895035,-162.566752)


def run_tests(input_data, input_variable, qc_config, output_path):
    # Run QC
    qc = QcConfig(qc_config)
    qc_results =  qc.run(
        inp=input_data[input_variable],
        tinp=input_data['timestamp'],
        zinp=input_data['z']
    )


    qc_result_pd = pd.DataFrame(qc_results["qartod"], columns=qc_results["qartod"].keys())
    result = pd.concat([input_data, qc_result_pd], axis=1)

    return result