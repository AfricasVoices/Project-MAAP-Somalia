import argparse
import csv
import time
from core_data_modules.traced_data import TracedData, Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO

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
        trace_pdm1_input_path = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm2_input_path, 'r') as f:
        trace_pdm2 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm3_input_path, 'r') as f:
        trace_pdm3 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm4_input_path, 'r') as f:
        trace_pdm4 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm5_input_path, 'r') as f:
        trace_pdm5 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    
    #concatenate the PDMs
    trace_combined = []
    for trace_data in trace_pdm1_input_path:
        trace_combined.append(trace_data)
    for trace_data in trace_pdm2:
        trace_combined.append(trace_data)
    for trace_data in trace_pdm3:
        trace_combined.append(trace_data)
    for trace_data in trace_pdm4:
        trace_combined.append(trace_data)
    for trace_data in trace_pdm5:
        trace_combined.append(trace_data)
    
    with open(traced_json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(trace_combined, f, pretty_print=True)
