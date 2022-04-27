import io
import param
import panel as pn
import pandas as pd

class FileInput(param.Parameterized):
    data = param.DataFrame()
    
    file_input = param.Parameter()
    
    def __init__(self, **params):
        super().__init__(file_input=pn.widgets.FileInput(), **params)

    @pn.depends("file_input.value", watch=True)
    def _parse_file_input(self):
        value = self.file_input.value
        if value:
            string_io = io.StringIO(value.decode("utf8"))
            self.data = pd.read_csv(string_io, parse_dates=["Time"])
        else:
            print("error")
        
    def view(self):
        return pn.Column(
            "## Upload and Plot Data",
            self.file_input
        )
    
file_input = FileInput()

file_input_view = file_input.view()
file_input_view

pn.template.FastListTemplate(site="Panel", title="Download and Upload CSV File", main=[ file_input_view,]).servable();