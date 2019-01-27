import time

import pytz  # Timezone library for converting datetime objects between timezones
from core_data_modules.cleaners import Codes
from core_data_modules.traced_data import Metadata
from dateutil.parser import isoparse


class AnalysisKeys(object):
    @staticmethod
    def set_matrix_keys(user, list_td, keys_to_matrix):
        '''
        :param user: Person running this program
        :type user: str
        :param list_td: List of TracedData Objects
        :type list_td: list
        :param keys_to_matrix: Dict of keys to convert to matrix and prefixes to add to the new keys
        :type keys_to_matrix: dict
        :return: List of keys that will be used to create the matrix
        :rtype: list
        '''
        matrix_keys = {
            'q1_education', 'q1_food', 'q1_childrens_needs', 'q1_family_needs', 'q1_health', 'q1_self_employment',
            'q1_amount_not_sufficient', 'q1_closure_of_roads', 'q1_drought', 'q1_aid_not_received', 'q1_access_to_aid',
            'q1_need_investment',
            'q2_prefer_current_modality', 'q2_safety', 'q2_access_and_use_mobile_phones', 'q2_easy_access',
            'q2_inclusive_access', 'q2_prevents_corruption', 'q2_long_queues', 'q2_security_concerns',
            'q2_delays_in_the_program', 'q2_distance', 'q2_other', 'q2_shelter',
            'q3_more_aid', 'q3_need_money', 'q3_need_food', 'q3_business', 'q3_rent', 'q3_clothes', 'q3_health_services',
            'q3_education', 'q3_water', 'q3_continuation_of_cash_transfer', 'q3_peace', 'q3_employment',
            'q4_opportunity_to_give_opinions', 'q4_not_received_cash', 'q4_lack_of_information',
        }

        for td in list_td:
            matrix_d = dict()
            for key, prefix in keys_to_matrix.items():
                if key in td:
                    if type(td[key]) is list:
                        for code in td[key]:
                            new_key = prefix + code
                            matrix_keys.add(new_key)
                            matrix_d[new_key] = Codes.MATRIX_1
                            td.append_data(matrix_d, Metadata(user, Metadata.get_call_location(), time.time()))
                    else:
                        # assumes that td[key] is a dict
                        new_key = prefix + td[key]
                        matrix_keys.add(new_key)
                        matrix_d[new_key] = Codes.MATRIX_1
            td.append_data(matrix_d, Metadata(user, Metadata.get_call_location(), time.time()))

        for td in list_td:
            matrix_d = dict()
            for key in matrix_keys:
                if key not in td:
                    matrix_d[key] = Codes.MATRIX_0
            td.append_data(matrix_d, Metadata(user, Metadata.get_call_location(), time.time()))

        return list(matrix_keys)

    @staticmethod
    def set_analysis_keys(user, list_td, key_map):
        '''
        :param user: Person running this program
        :type user: str
        :param list_td: List of TracedData Objects
        :type list_td: list
        :param key_map: Dict of key, value pairs to translate keys to. The key
                        is what the value will be converted to
        :type key_map: dict
        '''
        for td in list_td:
            td.append_data(
                {new_key: td[old_key] for new_key, old_key in key_map.items()
                if old_key in td},
                Metadata(user, Metadata.get_call_location(), time.time())
            )

    @staticmethod
    def arrange_keys(export_list):
        '''
        :param export_list: The list of keys that will be arranges according to the list below
        :type export_list: list
        '''
        how_to_arrange = [
            'UID', 'gender', 'gender_raw', 'age', 'age_raw', 'clan_identity', 'clan_identity_raw', 'household_size', 
            'scope_district',
            
            'needs_met_raw', 'needs_met_yesno', 'q1_access_to_aid', 'q1_aid_not_received', 'q1_aid_not_recieved',
            'q1_amount_not_sufficient', 'q1_childrens_needs', 'q1_closure_of_roads', 'q1_drought', 'q1_education',
            'q1_family_needs', 'q1_food', 'q1_health', 'q1_need_investment', 'q1_self_employment', 'q1_NA', 'q1_NR',
            
            'cash_modality_raw', 'cash_modality_yesno', 'q2_access_and_use_mobile_phones', 'q2_delays_in_the_program',
            'q2_distance', 'q2_easy_access', 'q2_inclusive_access', 'q2_long_queues', 'q2_other',
            'q2_prefer_current_modality', 'q2_prevents_corruption', 'q2_safety', 'q2_security_concerns', 'q2_NA',
            'q2_NR', 'q2_WS', 'q2_shelter',
            
            'community_priorities_raw', 'q3_business', 'q3_clothes', 'q3_continuation_of_cash_transfer', 'q3_education',
            'q3_employment', 'q3_health_services', 'q3_more_aid', 'q3_need_food', 'q3_need_money', 'q3_peace', 'q3_rent',
            'q3_water', 'q3_NA', 'q3_WS', 'q3_NC', 'q3_NR',
            
            'inclusion_raw', 'inclusion_yesno', 'q4_lack_of_information', 'q4_not_received_cash', 
            'q4_opportunity_to_give_opinions', 'q4_NA', 'q4_NR', 'q4_WS',
        ]
        # Check that we're not missing any keys in how_to_arrange
        set_difference = set(export_list) - set(how_to_arrange)
        assert len(set_difference) == 0, f'These keys are missing in how_to_arrange {set_difference}'

        export_list.sort(key=lambda x: how_to_arrange.index(x))
        return export_list

