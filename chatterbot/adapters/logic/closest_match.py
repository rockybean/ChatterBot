# -*- coding: utf-8 -*-
from .base_match import BaseMatchAdapter
from fuzzywuzzy import fuzz


class ClosestMatchAdapter(BaseMatchAdapter):
    """
    The ClosestMatchAdapter creates a response by
    using fuzzywuzzy's process class to extract the most similar
    response to the input. This adapter selects a response to an
    input statement by selecting the closest known matching
    statement based on the Levenshtein Distance between the text
    of each statement.
    """

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.context.storage.get_response_statements()

        if not statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        confidence = -1
        closest_match = input_statement

        # Find the closest matching known statement
        for statement in statement_list:
            ratio = fuzz.ratio(input_statement.text, statement.text)

            if ratio > confidence:
                confidence = ratio
                closest_match = statement

        '''
        closest_match, confidence = process.extractOne(
            input_statement.text,
            text_of_all_statements
        )
        '''

        # Convert the confidence integer to a percent
        confidence /= 100.0

        return confidence, closest_match

