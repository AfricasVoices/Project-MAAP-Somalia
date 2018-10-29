import argparse
import os
import random

from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCSVIO
from core_data_modules.util import IOUtils

# Number of messages to export in the ICR file
ICR_MESSAGES_COUNT = 200
# Number of characters below which messages are considered noise
NUMBER_OF_CHARS_NOISE = 15

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates files for inter-coder reliability")
    parser.add_argument(
        "user", help="User launching this program")
    parser.add_argument(
        "json_input_path", metavar="json-input-path",
        help="Path to the input JSON file, containing a list of serialized"
        "TracedData objects")
    parser.add_argument(
        "flow_name", metavar="flow-name",
        help="Name of activation flow from which this data was derived")
    parser.add_argument(
        "variable_name", metavar="variable-name",
        help="Name of message variable in flow")
    parser.add_argument(
        "icr_output_path", metavar="icr-output-path",
        help="Path to a CSV file to write 200 messages and run ids to, for use"
        " in inter-coder reliability evaluation")

    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    variable_name = args.variable_name
    flow_name = args.flow_name
    icr_output_path = args.icr_output_path

    # Load data from JSON file
    with open(json_input_path, "r") as f:
        show_messages = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Filter out test messages sent by AVF.
    show_messages = [td for td in show_messages
                     if not td.get("test_run", False)]

    # Filter for runs which contain the key with the variable name
    show_message_key = "{} (Text) - {}".format(variable_name, flow_name)
    show_messages = [td for td in show_messages
                     if show_message_key in td]

    not_noise = [td for td in show_messages
                 if len(td[show_message_key]) > NUMBER_OF_CHARS_NOISE]
    # Randomly select some messages to export for ICR
    random.seed(0)
    random.shuffle(not_noise)
    icr_messages = not_noise[:ICR_MESSAGES_COUNT]

    # Output ICR data to a CSV file
    run_id_key = "{} (Run ID) - {}".format(variable_name, flow_name)
    raw_text_key = "{} (Text) - {}".format(variable_name, flow_name)
    IOUtils.ensure_dirs_exist_for_file(icr_output_path)
    with open(icr_output_path, "w") as f:
        TracedDataCSVIO.export_traced_data_iterable_to_csv(
            icr_messages, f, headers=[run_id_key, raw_text_key])
