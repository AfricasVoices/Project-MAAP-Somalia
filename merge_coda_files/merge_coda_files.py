import argparse
import time
from os import path
import json
from dateutil.parser import isoparse

from core_data_modules.cleaners import CharacterCleaner, Codes
from core_data_modules.cleaners.codes import SomaliaCodes
from core_data_modules.cleaners.location_tools import SomaliaLocations
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCodaIO, TracedDataTheInterfaceIO
from core_data_modules.util import IOUtils


# TODO: remove once pull request for below merged with master in CoreDataModules
class TracedDataCoda2IO(object):
    @classmethod
    def import_coda_to_traced_data_iterable(cls, user, data, data_message_id_key, scheme_keys, f):
        '''
        Codes a 'column' of a collection of TracedData objects by using the codes from a Coda data-file.
        Data which is has not been assigned a code in the Coda file is coded using the NR code from the provided scheme.
        :param user: Identifier of user running this program.
        :type user: str
        :param data: TracedData objects to be coded using the Coda file.
        :type data: iterable of TracedData
        :param data_message_id_key: Key in TracedData objects of the message ids.
        :type data_message_id_key: str
        :param scheme_keys: Dictionary of of the key in each TracedData object of coded data for a scheme to
                            a Coda 2 scheme object.
        :type scheme_keys: dict of str -> list of dict
        :param f: Coda data file to import codes from.
        :type f: file-like
        '''
        # Build a lookup table of MessageID -> SchemeID -> Labels
        coda_dataset = dict()  # of MessageID -> (dict of SchemeID -> list of Label)
        for msg in json.load(f):
            schemes = dict()  # of SchemeID -> list of Label
            coda_dataset[msg['MessageID']] = schemes
            msg['Labels'].reverse()
            for label in msg['Labels']:
                scheme_id = label['SchemeID']
                if scheme_id not in schemes:
                    schemes[scheme_id] = []
                schemes[scheme_id].append(label)

        # Apply the labels from Coda to each TracedData item in data
        for td in data:
            for key_of_coded, scheme in scheme_keys.items():
                labels = coda_dataset.get(td[data_message_id_key], dict()).get(scheme[0]['SchemeID'])
                if labels is None:
                    not_reviewed_code_id = \
                        [code['CodeID'] for code in scheme[0]['Codes'] if 'CodeType' in code and code['CodeType'] == 'Control' 
                        and code['ControlCode'] == 'NR'] 
                        # TODO: issue for having CodeType key for every code
                    td.append_data(
                        {key_of_coded: {
                            'CodeID': not_reviewed_code_id,
                            'SchemeID': scheme[0]['SchemeID']
                            # TODO: Set the other keys which label would have had here had they come from Coda?
                        }},
                        Metadata(user, Metadata.get_call_location(), time.time())
                    )
                else:
                    for label in labels:
                        td.append_data(
                            {key_of_coded: label},
                            Metadata(label['Origin']['OriginID'], Metadata.get_call_location(),
                                     isoparse(label['DateTimeUTC']).timestamp())
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Merges manually cleaned files back into a traced data'
        'file.')
    parser.add_argument('user', help='User launching this program, for use by TracedData Metadata')
    parser.add_argument('json_input_path', metavar='json-input-path',
                        help='Path to JSON input file, which contains a list of TracedData objects')
    parser.add_argument(
        'flow_name', metavar='flow-name',
        help='Name of activation flow from which this data was derived')
    parser.add_argument(
        'variable_name', metavar='variable-name',
        help='Name of message variable in flow')
    parser.add_argument('coda_input_path', metavar='coda-input-path',
                        help='Manually-coded Coda file')
    parser.add_argument('traced_json_output_path', metavar='json-output-path',
                        help='Path to a JSON file to write merged results to')
    parser.add_argument('scheme_input_path', metavar='scheme-input-path',
                        help='Path to Coda scheme file used on coda file')
                        
    
    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    flow_name = args.flow_name
    variable_name = args.variable_name
    coda_input_path = args.coda_input_path
    traced_json_output_path = args.traced_json_output_path
    scheme_input_path = args.scheme_input_path

    # Load data from JSON file
    with open(json_input_path, 'r') as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Merge manually coded survey Coda files into the cleaned dataset
    if not path.exists(coda_input_path):
        raise NameError('Warning: No Coda file found')

    with open(scheme_input_path, 'r') as f:
        coding_scheme = json.load(f)

    show_message_key = '{} (Text) - {}'.format(variable_name, flow_name)
    coded_key = '{}_coded'.format(variable_name)
    with open(coda_input_path, 'r') as f:
        TracedDataCoda2IO.import_coda_to_traced_data_iterable(
            user, data, '{} MessageID'.format(show_message_key),
            {coded_key: coding_scheme}, f)

    # Write coded data back out to disk
    IOUtils.ensure_dirs_exist_for_file(traced_json_output_path)
    with open(traced_json_output_path, 'w') as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)
