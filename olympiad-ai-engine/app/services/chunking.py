import re

def split_into_concepts(text: str):
    concepts = re.split(r'Concept \d+:', text)
    cleaned = [c.strip() for c in concepts if len(c.strip()) > 200]
    return cleaned
