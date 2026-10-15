from collections import defaultdict
import itertools


def apriori(transactions, min_support_pct):
    """
    Функция алгоритма Apriori.
    """
    num_transactions = len(transactions)
    min_supp_count = (min_support_pct / 100.0) * num_transactions
    
    transaction_sets = [set(t) for t in transactions]
    all_frequent_itemsets = {}
    
    # L1
    item_counts = defaultdict(int)
    for t in transaction_sets:
        for item in t:
            item_counts[frozenset([item])] += 1
            
    current_L = {itemset: count for itemset, count in item_counts.items() if count >= min_supp_count}
    all_frequent_itemsets.update(current_L)
    
    # Lk
    k = 2
    while current_L:
        candidates = get_candidates(set(current_L.keys()), k)
        if not candidates:
            break
            
        candidate_counts = defaultdict(int)
        
        valid_transactions = [t for t in transaction_sets if len(t) >= k]
        
        for t in valid_transactions:
            for comb in itertools.combinations(t, k):
                c = frozenset(comb)
                if c in candidates:
                    candidate_counts[c] += 1
                    
        current_L = {c: count for c, count in candidate_counts.items() if count >= min_supp_count}
        all_frequent_itemsets.update(current_L)
        k += 1

    results = []
    for itemset, count in all_frequent_itemsets.items():
        supp_pct = (count / num_transactions) * 100
        results.append((itemset, supp_pct))
        
    return results

def get_candidates(Lk_minus_1, k):
    """
    Генерация кандидатов размера k на основе частых наборов размера k-1.
    """
    candidates = set()
    Lk_list = list(Lk_minus_1)
    
    for i in range(len(Lk_list)):
        for j in range(i + 1, len(Lk_list)):
            set1 = Lk_list[i]
            set2 = Lk_list[j]
            
            union_set = set1 | set2
            if len(union_set) == k:
                is_valid = True
                for item in union_set:
                    subset = union_set - frozenset([item])
                    if subset not in Lk_minus_1:
                        is_valid = False
                        break
                
                if is_valid:
                    candidates.add(union_set)
                    
    return candidates
