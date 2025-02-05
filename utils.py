import re

def search_cases(query, civil_cases, criminal_cases, family_cases):
    """Search cases for keywords from user input."""
    query_words = set(query.lower().split())

    def match_cases(case_list):
        return [case for case in case_list if any(word in case.lower() for word in query_words)]

    return {
        "Civil": match_cases(civil_cases),
        "Criminal": match_cases(criminal_cases),
        "Family": match_cases(family_cases),
    }