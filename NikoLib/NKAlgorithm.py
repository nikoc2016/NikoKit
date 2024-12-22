from difflib import SequenceMatcher
from collections import Counter
from math import sqrt

# LCS Similarity (Slowest)
def str_similarity_score_lcs(str1, str2):
    matcher = SequenceMatcher(None, str1, str2)
    return int(sum(block.size for block in matcher.get_matching_blocks() if block.size > 0))

# Cosine Similarity (Moderate)
def str_similarity_score_cosine(str1, str2):
    vec1, vec2 = Counter(str1), Counter(str2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum(vec1[char] * vec2[char] for char in intersection)
    norm1 = sqrt(sum(val ** 2 for val in vec1.values()))
    norm2 = sqrt(sum(val ** 2 for val in vec2.values()))
    return dot_product / (norm1 * norm2) if norm1 and norm2 else 0

# Jaccard Similarity (Fastest)
def str_similarity_score_jaccard(str1, str2):
    set1, set2 = set(str1), set(str2)
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0