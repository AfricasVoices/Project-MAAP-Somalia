import argparse
import csv
import time
from core_data_modules.traced_data import TracedData, Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loads the PDM surveys and concatenates them")
    parser.add_argument("pdm1", help="Path to the first PDM survey")
    parser.add_argument("pdm2", help="Path to the second PDM survey")
    parser.add_argument("pdm3", help="Path to the third PDM survey")
    parser.add_argument("pdm4", help="Path to the fourth PDM survey")
    parser.add_argument("pdm5", help="Path to the fifth PDM survey")
    parser.add_argument("trace_json_path", help="Path to concatenated TraceData JSON")
    parser.add_argument("user", help="Identifier of user launching this program, for use in TracedData Metadata")

    args = parser.parse_args()
    pdm1 = args.pdm1
    pdm2 = args.pdm2
    pdm3 = args.pdm3
    pdm4 = args.pdm4
    pdm5 = args.pdm5
    trace_json_path = args.trace_json_path
    user = args.user

    #load the 5 PDMs that were saved as JSON
    with open(pdm1, 'r') as f:
        trace_pdm1 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm2, 'r') as f:
        trace_pdm2 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm3, 'r') as f:
        trace_pdm3 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm4, 'r') as f:
        trace_pdm4 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    with open(pdm5, 'r') as f:
        trace_pdm5 = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    
    #concatenate the PDMs
    trace_combined = []
    for trace_data in trace_pdm1:
        trace_combined.append(trace_data)
    for trace_data in trace_pdm2:
        trace_combined.append(trace_data)
    for trace_data in trace_pdm3:
        trace_combined.append(trace_data)
    for trace_data in trace_pdm4:
        trace_combined.append(trace_data)
    for trace_data in trace_pdm5:
        trace_combined.append(trace_data)
    
    with open(trace_json_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(trace_combined, f, pretty_print=True)
