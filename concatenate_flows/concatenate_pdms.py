import argparse
import csv
import time
import re
from core_data_modules.traced_data import TracedData, Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO


def normalise_pdm_flow_keys(pdm_traced_data, key_to_normalise, normalised_key):
    """
    Normalises the keys from different PDMs(Post Distribuiton Monitoring survey)
    Acts on the TracedData Object itself(pdm_traced_data)

    :param pdm_traced_data: Data to normalise the keys of
    :type pdm_traced_data: iterable of TracedData
    :param key_to_normalise: Key to search for and normalise
    :type key_to_normalise: str
    :param normalised_key: String create new key from 
    :type normalised_key: str
    """
    for record in pdm_traced_data:
        data_to_append = {}
        for key in record.keys():
            if key_to_normalise in key:
                new_key = re.sub(key_to_normalise, normalised_key, key)
                data_to_append[new_key] = record[key]
        md =  Metadata(user, Metadata.get_call_location(), time.time())
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

    # load the 5 PDMs that were saved as JSON
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
    
    # normalise the keys
    normalise_pdm_flow_keys(traced_pdm1, 'emergency_maap_pdm1_survey', 'emergency_maap_pdm')
    normalise_pdm_flow_keys(traced_pdm2, 'emergency_maap_pdm2_survey', 'emergency_maap_pdm')
    normalise_pdm_flow_keys(traced_pdm3, 'emergency_maap_pdm3_survey', 'emergency_maap_pdm')
    normalise_pdm_flow_keys(traced_pdm4, 'emergency_maap_pdm4_survey', 'emergency_maap_pdm')
    normalise_pdm_flow_keys(traced_pdm5, 'emergency_maap_pdm5_survey', 'emergency_maap_pdm')


    # concatenate the PDMs
    pdm_combined = []
    pdm_combined.extend(traced_pdm1)
    pdm_combined.extend(traced_pdm2)
    pdm_combined.extend(traced_pdm3)
    pdm_combined.extend(traced_pdm4)
    pdm_combined.extend(traced_pdm5)

    with open(traced_json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(pdm_combined, f, pretty_print=True)
