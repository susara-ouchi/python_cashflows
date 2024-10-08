from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def LOAD_TABLES(*tables):

    """Update tables added to the table files

    tables: table files to be updated
    Example - LOAD_TABLES('table1', 'table2')

    returns 0
    """
    Path, os, openpyxl, pd = Input.Path, Input.os, Input.openpyxl, Input.pd

    for table in tables[0]:
        if not os.path.isabs(Path[table]):
            table_path = os.path.join(Path["Model"], Path[table])
        else:
            raise ValueError("relative path required for tables/excel range files")

        table_workbook = openpyxl.load_workbook(filename = table_path)
        for sheet in table_workbook.sheetnames:
            if sheet not in dir(LOAD_TABLES.parent):
                df = pd.read_excel(table_path, sheet_name = sheet, index_col = 0, header = 0)

                LOAD_TABLES.parent.new_pandas(data = df, file_type = "excel", name = sheet, path = Path[table], sheet = sheet)
                if eval(f"{sheet}.isnull().values.any()"):
                    status = "Wrn"
                else:
                    status = "OK"
                print(f"Loaded {sheet}... {status}")
    return 0


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("...",), "auto")

COH_2023_0 = ("IOSpec", 2763551950256, 2763551574336)

COH_2023_1 = ("IOSpec", 2763552909776, 2763551572608)