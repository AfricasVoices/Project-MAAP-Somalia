import argparse
import time
from os import path
import json
from dateutil.parser import isoparse

from core_data_modules.cleaners import Codes
from core_data_modules.cleaners.cleaning_utils import CleaningUtils
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCoda2IO
from core_data_modules.util import IOUtils
from core_data_modules.data_models import Scheme

# opens a coding scheme
def _open_scheme(filepath):
    with open(filepath, "r") as f:
        firebase_map = json.load(f)
        return Scheme.from_firebase_map(firebase_map)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Merges manually cleaned files back into a traced data'
        'file.')
    parser.add_argument('user', help='User launching this program')
    parser.add_argument('json_input_path', metavar='json-input-path',
                        help='Path to JSON input file TracedData objects')
    parser.add_argument('variable_name', metavar='variable-name',
                        help='Name of message variable in flow')
    parser.add_argument('coda_input_path', metavar='coda-input-path',
                        help='Manually-coded Coda file')
    parser.add_argument('traced_json_output_path', metavar='json-output-path',
                        help='Path to a JSON file to write merged results to')
    parser.add_argument('coding_scheme_path', metavar='coding-scheme-path',
                        help='Path to Coda scheme file used on coda file')
    parser.add_argument('is_yes_no', metavar='is-yes-no',
                        help='Is this variable a yes no question')
                        
    
    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    variable_name = args.variable_name
    coda_input_path = args.coda_input_path
    traced_json_output_path = args.traced_json_output_path
    coding_scheme_path = args.coding_scheme_path
    is_yes_no = args.is_yes_no

    # Load data from JSON file
    with open(json_input_path, 'r') as f:
        list_td = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    
    # Load the coding scheme
    code_scheme = _open_scheme(coding_scheme_path)


    # Merge manually coded survey Coda files into the cleaned dataset
    nr_label = CleaningUtils.make_cleaner_label(
                code_scheme, 
                code_scheme.get_code_with_control_code(Codes.NOT_REVIEWED),
                Metadata.get_call_location()
            )
    id_field = 'Cash_Modality_Yesno (Text) - emergency_maap_new_pdm_id'
    coded_key = '{}_coded'.format(variable_name.lower())

    if is_yes_no == 'True':
        is_yes_no = True
        yes_no_key = '{}_yesno'.format(variable_name.lower())
        yes_no_scheme = _open_scheme('Yes_No.json')
    else:
        is_yes_no = False

    if is_yes_no:
        coding_schemes = {
            coded_key: code_scheme,
            yes_no_key: yes_no_scheme,
        }
    else:   
        coding_schemes = {
            coded_key: code_scheme,
        }
    with open(coda_input_path, "r") as f:
        TracedDataCoda2IO.import_coda_2_to_traced_data_iterable(
            user, list_td, id_field, coding_schemes, nr_label, f)
    
    # Write coded data back out to disk
    IOUtils.ensure_dirs_exist_for_file(traced_json_output_path)
    with open(traced_json_output_path, 'w') as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(
            list_td, f, pretty_print=True)
