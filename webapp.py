import os
import time
import streamlit as st
from PIL import Image
from tools_1.run_methods import *

# Set initial theme in session state
st.session_state['theme'] = 'dark'

# Set the CSS based on the theme
st.set_page_config(page_title="Milliman Interactive User Space", page_icon="graphics/Milliman_logo_Li.ico", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #222b36;
    }
    .css-18e3th9, .css-1d391kg {
        background-color: #f4f4f4;
    }
    .css-1aumxhk, .css-1v3fvcr, .css-1h4f60p, h1, h2, h3, h4, h5, h6, p, label { 
        color: #FFFFFF;
    }
    .stButton button {
        background-color: #50bdff;
        color: #50BDFF;
        border: 1px solid #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main content
logo_path = r"graphics\Milliman_logo_Cloud.ico"
# logo_path = r"graphics\MIL-Corporate-Logo-Cloud2x.png"

logo = Image.open(logo_path)
st.image(logo, width=60)  # Adjust the width as needed  (60 for small log0, 120 for large logo)

currwd = os.path.dirname(__file__); os.chdir(currwd)
st.header("Milliman Interactive User Space")
# st.subheader("Cashflows Modelling using Python")

FileExtnSupported = [".xlsx", ".csv"]

st.write("This web-based GUI enables users to input files, configure run settings, and run actuarial models efficiently.")

# Tabs Setup
Models, Input = st.tabs(['Models', 'Input'])
# Models, Input, AboutUs = st.tabs(['Models', 'Input', 'About Us'])

# Tab: Models
import streamlit as st
# Create a dictionary to map folder names to their aliases
model_aliases = {
    "1_Traditional": "Non-Par (Traditional) Product",
    "2_Participating": "Participating Product",
    "3_UnitLinked": "Unit Linked Product"
}

# Get the list of model folders
ModelsList_og = os.listdir("models")

# Use the mapping to create a list of aliases
ModelAliasesList = [model_aliases[model] for model in ModelsList_og if model in model_aliases]
# ModelsList = ModelAliasesList
ModelsList = ModelsList_og

ModelsCol1, ModelsCol2, ModelsCol3 = Models.columns(3)

with ModelsCol1:
    st.subheader("Select the models to run:")
    AllCheck = st.checkbox(label = "All", value = False)    
    for i in range(len(ModelsList)):
        exec(f"ModelCheck{i} = st.checkbox('{ModelAliasesList[i]}', value = AllCheck)")

with ModelsCol2:
    st.subheader("Run settings")
    OutputPath = st.text_input("Output Path", value = os.path.join(currwd,"results"))
    BatchSize = st.text_input("Maximum batchsize (cannot exceed 2x10^5)", value = 10000)
    StackTracing = st.checkbox("Stack Tracing (run-time report)", value = False)

with ModelsCol3:
    def RunModels():
        try:
            n = int(float(BatchSize))
        except ValueError:
            raise ValueError("Cannot convert this type into int")

        for i, model in zip(range(len(ModelsList)), ModelsList):
            if eval(f"ModelCheck{i} == True"):
                st.write("Running: " + os.path.join(currwd, "models", model))
                if StackTracing:
                    stack_tracing(os.path.join(currwd, "models", model), ExportCB, OutputPath, FileTypeRadio)
                else:
                    run_model(os.path.join(currwd, "models", model), ExportCB, OutputPath, n, FileTypeRadio)

    def CohortModels():
        for i, model in zip(range(len(ModelsList)), ModelsList):
            if eval(f"ModelCheck{i} == True"):
                st.write("Running: " + os.path.join(currwd, "models", model))
                st.write("Working")
                cohort_model(os.path.join(currwd, "models", model), OutputPath, FileTypeRadio)
            

    # def CohortModels():
    #     total_models = sum(eval(f"ModelCheck{i}") for i in range(len(ModelsList)))  # Count the total number of selected models
        
    #     if total_models == 0:
    #         st.warning("No models selected to run.")
    #         return

    #     completed_models = 0

    #     for i, model in zip(range(len(ModelsList)), ModelsList):
    #         if eval(f"ModelCheck{i} == True"):
    #             start_time = time.time()  # Record the start time
                
    #             st.write(f"Running: {os.path.join(currwd, 'models', model)}")
    #             cohort_model(os.path.join(currwd, "models", model), OutputPath, FileTypeRadio)
                
    #             elapsed_time = time.time() - start_time  # Calculate the elapsed time
    #             elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))  # Format the elapsed time
                
    #             completed_models += 1
    #             st.write(f"Completed: {os.path.join(currwd, 'models', model)} in {elapsed_time_str}")
        
    #     st.success("All selected models have been processed.")


    ModelsCol31, ModelsCol32 = ModelsCol3.columns(2)
    with ModelsCol31:
        ResultsButton = st.button("Aggregate", on_click = RunModels)
    with ModelsCol32:
        CohortButton = st.button("Cohort", on_click = CohortModels)
    
    st.write("Note: Batch-wise execution is not functional for Stack Tracing or Cohort")
    ExportCB = st.checkbox("Export aggregate results", value = True)        
    FileTypeRadio = st.radio("File type:", FileExtnSupported)

# Tab: Inputs
ModelsPath = os.path.join(currwd, "models")
ModelCount = 0; fPCount = 0 ## counting variables for all models and 'FilePaths'
with Input:
    n = len(os.listdir(ModelsPath))
    for i, ModelDir in zip(range(1, n+1), os.listdir(ModelsPath)):
        if ModelDir in model_aliases:  # Only include the first 3 models
            with st.expander(model_aliases[ModelDir]):
                ModelPath = os.path.join(ModelsPath, ModelDir)
                for subdir, dirs, files in os.walk(ModelPath):
                    for file in files:
                        if file.endswith(tuple(FileExtnSupported)):
                            ModelCount += 1; fPCount += 1
                            exec(f"filePath_{fPCount} = os.path.join(subdir, file)")
                            ButtonName = "".join((str(i), ' ', file.split(".")[0]))
                            exec(f"Button_{ModelCount} = st.button(ButtonName, on_click = lambda: os.startfile(filePath_{fPCount}))")

# Tab: About Us
# with AboutUs:
#     st.header("About Us")
#     st.write("""
#         Milliman is among the world's largest providers of actuarial and related products and services. 
#         We are dedicated to helping our clients protect the health and financial well-being of people everywhere.
#     """)
