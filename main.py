import multiprocessing
from pathlib import Path
from data_processing import process_profiles_batch
from collections import defaultdict

DATA_FOLDER = "profiles"
BATCH_SIZE = 1000
NUM_WORKERS = 4
TOTAL_DEVELOPERS = 10000

def main():
    all_files = list(Path(DATA_FOLDER).glob("*.json"))
    file_batches = [all_files[i:i + BATCH_SIZE] for i in range(0, len(all_files), BATCH_SIZE)]

    company_frequencies, skill_frequencies, global_company_skill_counts = defaultdict(int), defaultdict(int), defaultdict(int)

    with multiprocessing.Pool(NUM_WORKERS) as pool:
        results = pool.map(process_profiles_batch, file_batches)

    for _, _, batch_company_counts, batch_skill_counts, batch_company_skill_counts in results:
        for company, count in batch_company_counts.items():
            company_frequencies[company] += count

        for skill, count in batch_skill_counts.items():
            skill_frequencies[skill] += count

        for (company, skill), count in batch_company_skill_counts.items():
            global_company_skill_counts[(company, skill)] += count

    conditional_probabilities = {
        (company, skill): (global_company_skill_counts[(company, skill)] / TOTAL_DEVELOPERS) /(company_frequencies[company] /TOTAL_DEVELOPERS)
        for (company, skill) in global_company_skill_counts
        if company_frequencies[company] > 0
    }

    for (company, skill), prob in conditional_probabilities.items():
        print(f"P({skill} | {company}): {prob:.16f}")

if __name__ == "__main__":
    main()
