import pandas as pd
import numpy as np
from datetime import datetime

from ioos_qc.config import QcConfig
from ioos_qc import qartod

# Water level data
# For a fixed station in Kotzebue, AK (https://www.google.com/maps?q=66.895035,-162.566752)
from pathlib import Path
basedir = Path().absolute()
libdir = basedir.parent.parent.parent
filename = basedir.joinpath(input1)
variable_name=input2

# Load data
data = pd.read_csv(filename, parse_dates=['time'])

# Run QC
qc = QcConfig(qc_config)
qc_results =  qc.run(
    inp=data[input2],
    tinp=data['timestamp'],
    zinp=data['z']
)


qc_result_pd = pd.DataFrame(qc_results["qartod"], columns=qc_results["qartod"].keys())
result = pd.concat([data, qc_result_pd], axis=1)
result.to_csv(input3)

print("Done")
