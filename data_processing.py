from typing import List, Tuple, Dict, Set
from pathlib import Path
from collections import defaultdict
from file_utils import read_json_file

def process_profiles_batch(file_list: List[Path]) -> Tuple[Set[str], Set[str], Dict[str, int], Dict[str, int], Dict[Tuple[str, str], int]]:
    """Processes a batch of JSON profiles and extracts unique companies, skills, and their counts."""
    unique_companies, unique_skills = set(), set()
    company_counts, skill_counts = defaultdict(int), defaultdict(int)
    company_skill_counts = defaultdict(int)

    for file in file_list:
        profile = read_json_file(file)

        companies = set(profile.get("companies", []))
        skills = set(profile.get("skills", []))

        if len(companies) < 3:
            continue

        unique_companies.update(companies)
        unique_skills.update(skills)

        for company in companies:
            company_counts[company] += 1

        for skill in skills:
            skill_counts[skill] += 1

        for company in companies:
            for skill in skills:
                company_skill_counts[(company, skill)] += 1

    return unique_companies, unique_skills, dict(company_counts), dict(skill_counts), dict(company_skill_counts)
