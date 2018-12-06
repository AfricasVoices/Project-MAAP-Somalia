import argparse
import csv
import time
import re
from core_data_modules.traced_data import TracedData, Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO


def open_scope(filepath):
    """
    Generator that opens the csv and yields a row from it
    :param filepath: path to file containing SCOPE data
    :type filepath: string
    """
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            scopeid = row['scopeid']
            yield scopeid, row


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merges scope data, contact data into a TraceData "
        "object and outputs as a traced data file")
    parser.add_argument(
        "user", help="Identifier of user launching this program, for use in "
        "TracedData Metadata")
    parser.add_argument("trace_json_path", metavar="json-input-path",
                        help="Path to TraceData JSON")
    parser.add_argument("contact_json_path", metavar="contact-json-input-path",
                        help="Path to contact TraceData JSON")
    parser.add_argument("scope_csv_path", metavar="scope-csv-path",
                        help="Path to SCOPE CSV")
    parser.add_argument("traced_json_output_path", metavar="json-output-path",
                        help="Path to concatenated TraceData JSON")

    args = parser.parse_args()
    user = args.user
    trace_json_path = args.trace_json_path
    contact_json_path = args.contact_json_path
    scope_csv_path = args.scope_csv_path
    traced_json_output_path = args.traced_json_output_path

    # load in the trace data
    with open(trace_json_path, 'r') as f:
        td_list = TracedDataJsonIO.import_json_to_traced_data_iterable(f)
    # load in the contact trace data
    with open(contact_json_path, 'r') as f:
        contact_data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # append contact trace data to trace data
    for trace in td_list:
        for contact in contact_data:
            if (trace['avf_phone_id'] == contact['avf_phone_id'] and
                    'maapscopeid' in contact):
                trace.append_data({'maapscopeid': contact['maapscopeid']},
                                  Metadata(user,
                                           Metadata.get_call_location(),
                                           time.time()))
    # append SCOPE data to trace data
    for trace in td_list:
        if 'maapscopeid' in trace:
            # load in the SCOPE data
            scope_data = open_scope(scope_csv_path)
            for scope in scope_data:
                if trace['maapscopeid'] == scope[0]:
                    trace.append_data(dict(scope[1]),
                                      Metadata(user,
                                               Metadata.get_call_location(),
                                               time.time()))

    with open(traced_json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(td_list, f,
                                                             pretty_print=True)
