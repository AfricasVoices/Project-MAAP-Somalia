import argparse
import sys
import time

from core_data_modules.cleaners import Codes
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCSVIO
from core_data_modules.util.consent_utils import ConsentUtils
from core_data_modules.traced_data.util import FoldTracedData

from lib.analysis_keys import AnalysisKeys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates files for analysis from the cleaned and coded '
        'show and survey responses')
    parser.add_argument(
        'user', help='User launching this program')
    parser.add_argument(
        'json_input_path', metavar='json-input-path',
        help='Path to a coded JSON file, containing a list of serialized '
        'TracedData objects')
    parser.add_argument(
        'json_output_path', metavar='json-output-path',
        help='Path to a JSON file to write serialized TracedData items to '
        'after modification by this pipeline stage')
    parser.add_argument(
        'csv_by_message_output_path', metavar='csv-by-message-output-path',
        help='Analysis dataset where messages are the unit for analysis (i.e. '
        'one message per row)')
    parser.add_argument(
        'csv_by_individual_output_path', metavar='csv-by-individual-output-path',
        help='Analysis dataset where respondents are the unit for analysis '
        '(i.e. one respondent per row, with all their messages joined into a '
        'single cell).')

    args = parser.parse_args()
    user = args.user
    data_input_path = args.json_input_path
    json_output_path = args.json_output_path
    csv_by_message_output_path = args.csv_by_message_output_path
    csv_by_individual_output_path = args.csv_by_individual_output_path

    # Serializer is currently overflowing
    # TODO: Investigate/address the cause of this.
    sys.setrecursionlimit(10000)

    demog_keys = [
        'gender',
        'gender_raw',
        'age',
        'age_raw',
        'clan_identity',
        'clan_identity_raw']

    survey_keys = [
        'needs_met_yesno',
        'needs_met_raw',
        'cash_modality_yesno',
        'cash_modality_raw',
        'community_priorities_raw',
        'inclusion_yesno',
        'inclusion_raw']
    
    scope_keys = [
        'scope_district',
        'household_size']

    key_map = {
        'UID': 'avf_phone_id',
        'needs_met_raw': 'Needs_Met_Yesno (Text) - emergency_maap_new_pdm',
        'cash_modality_raw': 'Cash_Modality_Yesno (Text) - emergency_maap_new_pdm',
        'community_priorities_raw': 'Community_Priorities (Text) - emergency_maap_new_pdm',
        'inclusion_raw': 'Inclusion_Yes_No (Text) - emergency_maap_new_pdm',
        
        'gender_raw': 'Gender (Text) - emergency_maap_new_demogs',
        'age_raw': 'Age (Text) - emergency_maap_new_demogs',
        'clan_identity_raw': 'Clan (Text) - emergency_maap_new_demogs',
        
        'scope_district': 'District',
        'household_size': 'Household Size'}

    # Load cleaned and coded message/survey data
    with open(data_input_path, 'r') as f:
        list_td = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    keys_to_matrix_convert = {
        'needs_met_reason': 'q1_',
        'cash_modality_reason': 'q2_',
        'community_priorities': 'q3_',
        'inclusion_reason': 'q4_',
    }

    # Get the matrix keys
    matrix_keys = AnalysisKeys.set_matrix_keys(user, list_td, keys_to_matrix_convert)

    # Translate keys to final values for analysis
    AnalysisKeys.set_analysis_keys(user, list_td, key_map)

    equal_keys = ['UID']
    equal_keys.extend(demog_keys)

    yes_no_keys = [
        'needs_met_yesno',
        'cash_modality_yesno',
        'inclusion_yesno']
    concat_keys = [
        'main_needs_raw',
        'cash_modality_raw',
        'community_priorities_raw',
        'needs_met_reason_raw',
        'inclusion_raw']

    export_keys = ['UID']
    export_keys.extend(demog_keys)
    export_keys.extend(survey_keys)
    export_keys.extend(matrix_keys)
    export_keys.extend(scope_keys)

    # Fold data to have one respondent per row
    to_be_folded = []
    for td in list_td:
        to_be_folded.append(td.copy())

    folded_data = FoldTracedData.fold_iterable_of_traced_data(
        user, to_be_folded, fold_id_fn=lambda td: td['UID'],
        equal_keys=equal_keys, concat_keys=concat_keys,
        matrix_keys=matrix_keys, yes_no_keys=yes_no_keys)

    # Output to CSV with one message per row
    with open(csv_by_message_output_path, 'w') as f:
        TracedDataCSVIO.export_traced_data_iterable_to_csv(list_td, f, headers=export_keys)
    
    # Output to CSV with one individual per row
    with open(csv_by_individual_output_path, "w") as f:
        TracedDataCSVIO.export_traced_data_iterable_to_csv(folded_data, f, headers=export_keys)

    # Export JSON
    with open(json_output_path, 'w') as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(folded_data, f, pretty_print=True)
