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
def open_scheme(filepath):
    with open(filepath, "r") as f:
        firebase_map = json.load(f)
        return Scheme.from_firebase_map(firebase_map)

def coda_id_to_strings(key_map, code_scheme, list_td):
    '''
    Converts CODA code IDs to strings
    :param key_map: Dict of key, value pairs to translate keys to. The key
                    is what the value will be converted to
    :type key_map: dict
    :param code_scheme: Coding scheme that contains the codes
    :type code_scheme: Scheme
    :param list_td: List of TracedData Objects
    :type list_td: list
    '''
    list_code_ids = [code.code_id for code in code_scheme.codes]
    for td in list_td:
        td.append_data(
            {new_key: code_scheme.get_code_with_id(td[old_key]["CodeID"]).string_value
            for new_key, old_key in key_map.items()
            if old_key in td and td[old_key]["CodeID"] in list_code_ids},
            Metadata(user, Metadata.get_call_location(), time.time())
        )

KEY_MAP = {
    'needs_met_reason': 'needs_met_yesno_coded',
    'needs_met_yesno': 'needs_met_yesno_yesno',
    
    'cash_modality_reason': 'cash_modality_yesno_coded',
    'cash_modality_yesno': 'cash_modality_yesno_yesno',
    
    'community_priorities': 'community_priorities_coded',
    
    'inclusion_reason': 'inclusion_yesno_coded',
    'inclusion_yesno': 'inclusion_yesno_yesno',
    
    'gender': 'gender_coded',
    'age': 'age_coded',
    'clan_identity': 'clan_coded',
}    

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
    parser.add_argument('coding_scheme_path', metavar='coding-scheme-path',
                        help='Path to Coda scheme file used on coda file')
    parser.add_argument('traced_json_output_path', metavar='json-output-path',
                        help='Path to a JSON file to write merged results to')
    # There is only one Yes/No coding scheme, it is used across this project
    parser.add_argument('has_yes_no', metavar='has-yes-no',
                        help='Is this variable a yes no question')
                        
    
    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    variable_name = args.variable_name
    coda_input_path = args.coda_input_path
    coding_scheme_path = args.coding_scheme_path
    traced_json_output_path = args.traced_json_output_path
    if args.has_yes_no == 'True':
        has_yes_no = True
    elif args.has_yes_no == 'False':
        has_yes_no = False
    else:
        raise Exception('<has-yes-no> only takes the strings "True" or "False"')

    # Load data from JSON file
    with open(json_input_path, 'r') as f:
        list_td = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    
    # Load the coding scheme
    code_scheme = open_scheme(coding_scheme_path)

    # Merge manually coded survey Coda files into the cleaned dataset
    nr_label = CleaningUtils.make_cleaner_label(
                code_scheme, 
                code_scheme.get_code_with_control_code(Codes.NOT_REVIEWED),
                Metadata.get_call_location()
            )
    id_field = '{}_id'.format(variable_name.lower())
    coded_key = '{}_coded'.format(variable_name.lower())

    if has_yes_no:
        yes_no_key = '{}_yesno'.format(variable_name.lower())
        yes_no_scheme = open_scheme('../coding_schemes/Yes_No.json')
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
    for key, code_scheme in coding_schemes.items():
        coda_id_to_strings(KEY_MAP, code_scheme, list_td)
    
    # Write coded data back out to disk
    IOUtils.ensure_dirs_exist_for_file(traced_json_output_path)
    with open(traced_json_output_path, 'w') as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(
            list_td, f, pretty_print=True)
