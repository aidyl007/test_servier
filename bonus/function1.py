from collections import defaultdict
import json

def get_journal_with_max_unique_drugs(data):
    # create a mapping from journal titles to a set of unique drug names
    journal_drug_map = defaultdict(set)

    # create journal-drug mapping with drug and journal fields
    for entry in data:
        drug = entry['drug']
        journal = entry['journal']
        journal_drug_map[journal].add(drug)

    # Initialize vars to search for journal with the highest number of unique drugs
    max_unique_drug_count = 0
    journal_with_max_drugs = None

    # check each journal's unique drugs to determine the one with the most
    for journal, unique_drugs in journal_drug_map.items():
        unique_drug_count = len(unique_drugs)
        if unique_drug_count > max_unique_drug_count:
            max_unique_drug_count = unique_drug_count
            journal_with_max_drugs = journal

    return journal_with_max_drugs, max_unique_drug_count


if __name__ == '__main__':
    try:
        with open('result.json', 'r') as file:
            data = json.load(file)  
            journal_with_max_drugs, max_unique_drug_count= get_journal_with_max_unique_drugs(data)
            print(f"The journal with the highest number of different drugs is '{journal_with_max_drugs}' with {max_unique_drug_count} unique drugs")

    except Exception as e:
        print(f"An error occurred: {e}")

