import streamlit.web.cli as cli
import sys
import os

os.chdir(os.path.dirname(__file__))

sys.argv = ['tools/streamlit.exe','run','webapp.py']

cli.main()