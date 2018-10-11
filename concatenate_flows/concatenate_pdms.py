import argparse
import csv
import time
import re
from core_data_modules.traced_data import TracedData, Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO


def key_normalisation(td_pdm, string_to_replace, replacement_string):
    """
    Used to normlise the keys from different PDMs. Acts to the TracedData
    Object itself(td_pdm)

    :param td_pdm: Data to normalise the keys of
    :type td_pdm:TracedData object
    :param string_to_replace: String to search for and replace
    :type string_to_replace: str
    :param replacement_string: String create new key from 
    :type replacement_string: str
    """
    md =  Metadata(user, Metadata.get_call_location(), time.time())
    for record in td_pdm:
        print(len(record))
        data_to_append = {}
        for key in record.keys():
            if string_to_replace in key:
                new_key = re.sub(string_to_replace, replacement_string, key)
                data_to_append[new_key] = record[key]
        record.append_data(data_to_append, md)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loads the PDM surveys and concatenates them")
    parser.add_argument("user", help="Identifier of user launching this program, for use in TracedData Metadata")
    parser.add_argument("pdm1_input_path", help="Path to the first PDM survey")
    parser.add_argument("pdm2_input_path", help="Path to the second PDM survey")
    parser.add_argument("pdm3_input_path", help="Path to the third PDM survey")
    parser.add_argument("pdm4_input_path", help="Path to the fourth PDM survey")
    parser.add_argument("pdm5_input_path", help="Path to the fifth PDM survey")
    parser.add_argument("traced_json_output_path", help="Path to concatenated TraceData JSON")
 
    args = parser.parse_args()
    user = args.user
    pdm1_input_path = args.pdm1_input_path
    pdm2_input_path = args.pdm2_input_path
    pdm3_input_path = args.pdm3_input_path
    pdm4_input_path = args.pdm4_input_path
    pdm5_input_path = args.pdm5_input_path
    traced_json_output_path = args.traced_json_output_path

    #load the 5 PDMs that were saved as JSON
    with open(pdm1_input_path, 'r') as f:
        traced_pdm1 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm2_input_path, 'r') as f:
        traced_pdm2 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm3_input_path, 'r') as f:
        traced_pdm3 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm4_input_path, 'r') as f:
        traced_pdm4 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm5_input_path, 'r') as f:
        traced_pdm5 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    
    #normalise the keys
    key_normalisation(traced_pdm1, 'emergency_maap_pdm1_survey', 'emergency_maap_pdm')
    key_normalisation(traced_pdm2, 'emergency_maap_pdm2_survey', 'emergency_maap_pdm')
    key_normalisation(traced_pdm3, 'emergency_maap_pdm3_survey', 'emergency_maap_pdm')
    key_normalisation(traced_pdm4, 'emergency_maap_pdm4_survey', 'emergency_maap_pdm')
    key_normalisation(traced_pdm5, 'emergency_maap_pdm5_survey', 'emergency_maap_pdm')


    #concatenate the PDMs
    trace_combined = []
    for trace_data in traced_pdm1:
        trace_combined.append(trace_data)
    for trace_data in traced_pdm2:
        trace_combined.append(trace_data)
    for trace_data in traced_pdm3:
        trace_combined.append(trace_data)
    for trace_data in traced_pdm4:
        trace_combined.append(trace_data)
    for trace_data in traced_pdm5:
        trace_combined.append(trace_data)
    
    with open(traced_json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(trace_combined, f, pretty_print=True)
