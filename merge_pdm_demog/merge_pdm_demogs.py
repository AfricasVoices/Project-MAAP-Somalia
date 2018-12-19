import argparse
from core_data_modules.traced_data import TracedData
from core_data_modules.traced_data.io import TracedDataJsonIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merges scope data, contact data into a TraceData "
        "object and outputs as a traced data file")
    parser.add_argument(
        "user", help="Identifier of user launching this program, for use in "
        "TracedData Metadata")
    parser.add_argument("pdm_path", metavar="pdm-path",
                        help="Path to PDM TraceData JSON")
    parser.add_argument("demogs_path", metavar="demogs-path",
                        help="Path to Demographics TraceData JSON")
    parser.add_argument("traced_json_output_path", metavar="json-output-path",
                        help="Path to concatenated TraceData JSON")

    args = parser.parse_args()
    user = args.user
    pdm_path = args.pdm_path
    demogs_path = args.demogs_path
    traced_json_output_path = args.traced_json_output_path

    with open(pdm_path, 'r') as f:
        pdm_td = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    with open(demogs_path, 'r') as f:
        demogs_td = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    TracedData.update_iterable(user, "avf_phone_id", pdm_td, demogs_td, "demogs")
    with open(traced_json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(pdm_td, f,
                                                             pretty_print=True)
