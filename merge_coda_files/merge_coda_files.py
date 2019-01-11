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

def coda_id_to_strings(list_td, old_key, key_map, code_scheme):
    '''
    Converts CODA code IDs to strings
    :param list_td: List of TracedData Objects
    :type list_td: list
    :param old_key: Key to be converted
    :type old_key: str
    :param key_map: Dict of key, value pairs to translate keys to. The value
                    is what the key will be converted to. Old_key will be
                    converted from this list.
    :type key_map: dict
    :param code_scheme: Coding scheme that contains the codes
    :type code_scheme: Scheme
    '''
    new_key = key_map[old_key]

    for td in list_td:
        if old_key in td:
            if type(td[old_key]) is list:
                list_code_strings = list()
                for code in td[old_key]:
                    code_string = code_scheme.get_code_with_id(code["CodeID"]).string_value
                    list_code_strings.append(code_string)
                td.append_data(
                    {new_key: list_code_strings},
                    Metadata(user, Metadata.get_call_location(), time.time())
                )
            else:
                td.append_data(
                    {new_key: code_scheme.get_code_with_id(td[old_key]["CodeID"]).string_value},
                    Metadata(user, Metadata.get_call_location(), time.time())
                )

def choose_coda_importer(is_multi_coded):
    """
    Depending on if the CODA file being merged is has multiple codes chooses the
    import function from core data to merge it with.
    
    :param is_multi_coded: Is this variable in the CODA file multi-coded
    :type is_multi_coded: bool
    """
    if is_multi_coded:
        with open(coda_input_path, "r") as f:
            TracedDataCoda2IO.import_coda_2_to_traced_data_iterable_multi_coded(
                user, list_td, id_field, {coded_key: code_scheme}, f)
    else:
        with open(coda_input_path, "r") as f:
            TracedDataCoda2IO.import_coda_2_to_traced_data_iterable(
                user, list_td, id_field, {coded_key: code_scheme}, f)

KEY_MAP = {
    'needs_met_yesno_coded': 'needs_met_reason',
    'needs_met_yesno_yesno': 'needs_met_yesno' ,

    'cash_modality_yesno_coded':'cash_modality_reason',
    'cash_modality_yesno_yesno':'cash_modality_yesno',

    'community_priorities_coded':'community_priorities',

    'inclusion_yes_no_coded':'inclusion_reason',
    'inclusion_yes_no_yesno':'inclusion_yesno',

    'gender_coded': 'gender',
    'age_coded': 'age',
    'clan_coded': 'clan_identity',
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
    parser.add_argument(
        'is_multi_coded', type=str, choices=['True','False'], metavar='is-multi-coded',
        help='Is this variable multi-coded')
    # There is only one Yes/No coding scheme, it is used across this project
    parser.add_argument(
        'has_yes_no', type=str, choices=['True','False'], metavar='has-yes-no',
        help='Is this variable a yes no question')
                        
    
    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    variable_name = args.variable_name
    coda_input_path = args.coda_input_path
    coding_scheme_path = args.coding_scheme_path
    traced_json_output_path = args.traced_json_output_path
    if args.is_multi_coded == 'True':
        is_multi_coded = True
    elif args.is_multi_coded == 'False':
        is_multi_coded = False
    if args.has_yes_no == 'True':
        has_yes_no = True
    elif args.has_yes_no == 'False':
        has_yes_no = False

    # Load data from JSON file
    with open(json_input_path, 'r') as f:
        list_td = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    
    # Load the coding scheme
    code_scheme = open_scheme(coding_scheme_path)

    # Merge manually coded survey Coda files into the cleaned dataset
    #nr_label = CleaningUtils.make_cleaner_label(
    #            code_scheme, 
    #            code_scheme.get_code_with_control_code(Codes.NOT_REVIEWED),
    #            Metadata.get_call_location()
    #        )
    id_field = '{}_id'.format(variable_name.lower())
    coded_key = '{}_coded'.format(variable_name.lower())

    if has_yes_no:
        yes_no_key = '{}_yesno'.format(variable_name.lower())
        yes_no_scheme = open_scheme('../coding_schemes/Yes_No.json')
        coding_schemes = {
            yes_no_key: yes_no_scheme,
            coded_key: code_scheme,
        }
        with open(coda_input_path, "r") as f:
            TracedDataCoda2IO.import_coda_2_to_traced_data_iterable(
                user, list_td, id_field, {yes_no_key: yes_no_scheme}, f)
        choose_coda_importer(is_multi_coded)
    else:   
        coding_schemes = {
            coded_key: code_scheme,
        }
        choose_coda_importer(is_multi_coded)

    # Convert the old keys
    for old_key, code_scheme in coding_schemes.items():
        coda_id_to_strings(list_td, old_key, KEY_MAP, code_scheme)
    
    # Write coded data back out to disk
    IOUtils.ensure_dirs_exist_for_file(traced_json_output_path)
    with open(traced_json_output_path, 'w') as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(
            list_td, f, pretty_print=True)
