import argparse
import os
import time
from os import path
import json

from core_data_modules.cleaners import somali, Codes
from core_data_modules.traced_data import Metadata, TracedData
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCoda2IO
from core_data_modules.util import IOUtils
from core_data_modules.cleaners.cleaning_utils import CleaningUtils
from core_data_modules.data_models import Scheme

# opens a coding scheme
def open_scheme(filepath):

    with open(filepath, "r") as f:
        firebase_map = json.load(f)
        return Scheme.from_firebase_map(firebase_map)

#Autocleaners that exist for this project
AUTO_CLEANERS = {'gender':somali.DemographicCleaner.clean_gender,
                'age':lambda x: str(somali.DemographicCleaner.clean_age(x)),
                'yes_no':somali.DemographicCleaner.clean_yes_no,
                }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Takes a TracedData json file, cleans the data and'
        'converts it to a CODAv2 file for verfication and manual coding')
    parser.add_argument(
        'user', help='User launching this program')
    parser.add_argument(
        'json_input_path', metavar='json-input-path',
        help='Path to the input JSON file, containing a list of serialized'
        'TracedData objects')
    parser.add_argument(
        'flow_name', metavar='flow-name',
        help='Name of activation flow from which this data was derived')
    parser.add_argument(
        'variable_name', metavar='variable-name',
        help='Name of message variable in flow')
    parser.add_argument(
        'traced_json_output_path', metavar='json-output-path',
        help='Path to concatenated TraceData JSON')
    parser.add_argument(
        'coda_output_path', metavar='coda-output-path',
        help='Path to a Coda file to write processed messages to')
    parser.add_argument(
        'coding_scheme_path', metavar='coding-scheme',
        help='Path to coding scheme that is for this data')
    parser.add_argument(
        'has_yes_no', type=str, choices=['True','False'], metavar='has-yes-no',
        help='Is this variable a yes no question')
    parser.add_argument(
        'auto_cleaner', metavar='auto-cleaner',
        help='automated cleaner to apply to this data')

    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    flow_name = args.flow_name
    variable_name = args.variable_name
    traced_json_output_path = args.traced_json_output_path
    coda_output_path = args.coda_output_path
    coding_scheme_path = args.coding_scheme_path
    if args.has_yes_no == 'True':
        has_yes_no = True
    elif args.has_yes_no == 'False':
        has_yes_no = False
    if args.auto_cleaner in AUTO_CLEANERS.keys():
        auto_cleaner = AUTO_CLEANERS[args.auto_cleaner]
    elif args.auto_cleaner == 'None':
        auto_cleaner = None
    else:
        raise Exception('There is no matching cleaner for: {}. If there is not autocleaner use the option "None"'.format(args.auto_cleaner))

    # Load in the coding scheme
    code_scheme = open_scheme(coding_scheme_path)


    # Load traced data list from JSON file
    with open(json_input_path, 'r') as f:
        list_td = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Filter out test messages sent by AVF.
    list_td = [td for td in list_td if not td.get('test_run', False)]

    # Keys used in the script
    message_key = '{} (Text) - {}'.format(variable_name, flow_name)
    coded_key = '{}_coded'.format(variable_name.lower())
    id_field = '{}_id'.format(variable_name.lower())
    time_key = '{} (Time) - {}'.format(variable_name, flow_name)
    if has_yes_no:
        yes_no_key = '{}_yesno'.format(variable_name.lower())
        yes_no_scheme = open_scheme('../coding_schemes/Yes_No.json')
        yes_no_cleaner = AUTO_CLEANERS['yes_no']
    else:
        yes_no_cleaner = None

    # Label data missing the key as true_missing
    # Data with empty strings will also be labelled true missing
    # create list that will be output to coda
    coda_td = []
    for td in list_td:
        if td.get(message_key, '') == '':
            missing_dict = dict()
            na_label = CleaningUtils.make_cleaner_label(
                        code_scheme,
                        code_scheme.get_code_with_control_code(
                            Codes.TRUE_MISSING),
                        Metadata.get_call_location()
                    )
            missing_dict[coded_key] = na_label.to_dict()
            if has_yes_no:
                na_label = CleaningUtils.make_cleaner_label(
                        yes_no_scheme,
                        yes_no_scheme.get_code_with_control_code(
                            Codes.TRUE_MISSING),
                        Metadata.get_call_location()
                    )
                missing_dict[yes_no_key] = na_label.to_dict()
            td.append_data(
                missing_dict, 
                Metadata(user, Metadata.get_call_location(), time.time())
                )
        else:
            coda_td.append(td)
        
    # Auto-coding data
    if auto_cleaner is not None:
        CleaningUtils.apply_cleaner_to_traced_data_iterable(
            user, list_td, message_key, coded_key, auto_cleaner, code_scheme)
    if yes_no_cleaner is not None:
        CleaningUtils.apply_cleaner_to_traced_data_iterable(
            user, list_td, message_key, yes_no_key, yes_no_cleaner, yes_no_scheme)

    # Appends a message id to each object in the provided iterable of TracedData.
    TracedDataCoda2IO.add_message_ids(user, list_td, message_key, id_field)

    # Output the CODA file for coded
    IOUtils.ensure_dirs_exist_for_file(coda_output_path)
    if has_yes_no:
        coding_schemes = {
            coded_key: code_scheme,
            yes_no_key: yes_no_scheme,
        }
    else:   
        coding_schemes = {
            coded_key: code_scheme,
        }
    with open(coda_output_path, "w") as f:
        TracedDataCoda2IO.export_traced_data_iterable_to_coda_2(
            coda_td, message_key, time_key, id_field, coding_schemes, f
        )

    # Write list of trace data to json output
    IOUtils.ensure_dirs_exist_for_file(traced_json_output_path)
    with open(traced_json_output_path, 'w') as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(list_td, f,
                                                             pretty_print=True)
