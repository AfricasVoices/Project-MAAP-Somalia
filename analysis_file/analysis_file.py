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
        'messages_input_dir', metavar='messages-input-dir',
        help='Path to a directory containing JSON files of responses to each '
        'of the shows in this project. Each JSON file should contain a list '
        'of serialized TracedData objects')
    parser.add_argument(
        'survey_input_path', metavar='survey-input-path',
        help='Path to a coded survey JSON file, containing a list of '
        'serialized TracedData objects')
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
    data_input_path = args.survey_input_path
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
        'selection_satisfaction_reason',
        'selection_satisfaction_yesno',
        'selection_satisfaction_reason_raw',
        'cash_modality_yesno',
        'cash_modality_reason',
        'cash_modality_reason_raw',
        'main_needs',
        'needs_met_yesno',
        'main_needs_raw',
        'needs_met_reason',
        'needs_met_reason_raw',
        'programme_recommendation',
        'programme_recommendation_raw']
    
    scope_keys = [
        'scope_district',
        'HH_size',
        'Receipt_yesno']
    
    key_map = {
        'UID': 'avf_phone_id',
        'selection_satisfaction_reason_raw': 'Selection_Satisfaction_Yesno (Text) - emergency_maap_pdm',
        'cash_modality_reason_raw': 'Cash_Modality_Yesno (Text) - emergency_maap_pdm',
        'main_needs_raw': 'Main_Needs (Text) - emergency_maap_pdm',
        'needs_met_reason_raw': 'Needs_Met_Yesno (Text) - emergency_maap_pdm',
        'programme_recommendation_raw': 'Programme_Recommendations (Text) - emergency_maap_pdm',
        'scope_district': 'District',
        'HH_size': 'Household Size'}

    # Load cleaned and coded message/survey data
    with open(data_input_path, 'r') as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Translate keys to final values for analysis
    AnalysisKeys.set_analysis_keys(user, data, key_map)

    equal_keys = ['UID']
    equal_keys.extend(demog_keys)

    yes_no_keys = [
        'selection_satisfaction_yesno',
        'cash_modality_yesno',
        'needs_met_yesno']
    concat_keys = [
        'selection_satisfaction_reason_raw',
        'cash_modality_reason_raw',
        'main_needs_raw',
        'needs_met_reason_raw',
        'programme_recommendation_raw']
    

    # Export to CSV
    export_keys = ['UID']
    export_keys.extend(demog_keys)
    export_keys.extend(survey_keys)
    export_keys.extend(scope_keys)


    # Fold data to have one respondent per row
    to_be_folded = []
    for td in data:
        to_be_folded.append(td.copy())

    folded_data = FoldTracedData.fold_iterable_of_traced_data(
        user, data, fold_id_fn=lambda td: td['UID'],
        equal_keys=equal_keys, concat_keys=concat_keys, yes_no_keys=yes_no_keys)

    # Output to CSV with one message per row
    with open(csv_by_message_output_path, 'w') as f:
        TracedDataCSVIO.export_traced_data_iterable_to_csv(data, f, headers=export_keys)

    # Export JSON
    with open(json_output_path, 'w') as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(folded_data, f, pretty_print=True)
