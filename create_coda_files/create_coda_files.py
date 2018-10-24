import argparse
import os
import time
import random

import pytz
from core_data_modules.cleaners import somali
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCodaIO
from core_data_modules.util import IOUtils
from dateutil.parser import isoparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes a TracedData json file and converts it to a CODA file")
    parser.add_argument("user", help="User launching this program")
    parser.add_argument("json_input_path", metavar="json-input-path",
                        help="Path to the input JSON file, containing a list of serialized TracedData objects")
    parser.add_argument("flow_name", metavar="flow-name",
                        help="Name of activation flow from which this data was derived")
    parser.add_argument("variable_name", metavar="variable-name",
                        help="Name of message variable in flow")
    parser.add_argument("coda_output_path", metavar="coda-output-path",
                        help="Path to a Coda file to write processed messages to")
    parser.add_argument("prev_coda_path", metavar="prev-coda-path",
                        help="Path to a Coda file containing previously coded messages")

    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    flow_name = args.flow_name
    variable_name = args.variable_name
    coda_output_path = args.coda_output_path
    prev_coda_path = args.prev_coda_path
    if os.path.exists(prev_coda_path):
        pass
    else:
        prev_coda_path = None

    # Load data from JSON file
    with open(json_input_path, "r") as f:
        show_messages = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Filter out test messages sent by AVF.
    show_messages = [td for td in show_messages if not td.get("test_run", False)]

    # Filter for runs which contain this key.
    show_message_key = "{} (Text) - {}".format(variable_name, flow_name)
    show_messages = [td for td in show_messages if show_message_key in td]

    # Convert date/time of messages to EAT
    utc_key = "{} (Time) - {}".format(variable_name, flow_name)
    eat_key = "{} (Time EAT) - {}".format(variable_name, flow_name)

    for td in show_messages:
        utc_time = isoparse(td[utc_key])
        eat_time = utc_time.astimezone(pytz.timezone("Africa/Nairobi")).isoformat()

        td.append_data(
            {eat_key: eat_time},
            Metadata(user, Metadata.get_call_location(), time.time())
        )

    # Output messages to Coda
    IOUtils.ensure_dirs_exist_for_file(coda_output_path)
    if prev_coda_path:
        # TODO: Needs to be updated once there's a previous scheme
        scheme_keys = {}
        with open(coda_output_path, "w") as f, open(prev_coda_path, "r") as prev_f:
            TracedDataCodaIO.export_traced_data_iterable_to_coda_with_scheme(
                show_messages, show_message_key, scheme_keys, f, prev_f=prev_f)
    else:
        with open(coda_output_path, "w") as f:
            TracedDataCodaIO.export_traced_data_iterable_to_coda(show_messages, show_message_key, f)
