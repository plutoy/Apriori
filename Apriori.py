#Create a test dataset

river_sp={'A':frozenset({1,2,5}),'B':frozenset({2,4}),'C':frozenset({2,3}),'D':frozenset({1,2,4}),
          'E':frozenset({1,3}),'F':frozenset({2,3}),'G':frozenset({1,3}),'H':frozenset({1,2,3,5}),'I':frozenset({1,2,3})}

print (river_sp['A'])
samples= {frozenset({1}):6, frozenset({2}):7, frozenset({3}):6, frozenset({4}):2, frozenset({5}):2}
print (samples.keys())



from collections import defaultdict

def find_frequent_itemsets(favorable_reviews_by_users, k_1_itemsets, min_support, ct):
    counts = defaultdict(int)
    for user, reviews in favorable_reviews_by_users.items():
        for itemset in k_1_itemsets:
            if itemset.issubset(reviews):
                for other_reviewed_movie in reviews - itemset:
                    current_superset = itemset | frozenset((other_reviewed_movie,))
                    counts[current_superset] += 1
                    print("#SET:")
                    print(current_superset)
                    print("#COUNT")
                    print(counts[current_superset])
    return dict([(itemset, frequency/ct) for itemset, frequency in counts.items() if frequency/ct >= min_support])
    
import sys
frequent_itemsets = {}  
min_support = 2


frequent_itemsets[1] = samples

print("There are {} movies with more than {} favorable reviews".format(len(frequent_itemsets[1]), min_support))
sys.stdout.flush()
for k in range(2, 4):
    # Generate candidates of length k, using the frequent itemsets of length k-1
    # Only store the frequent itemsets
    cur_frequent_itemsets = find_frequent_itemsets(river_sp, frequent_itemsets[k-1],min_support,k)
    print(cur_frequent_itemsets)
    if len(cur_frequent_itemsets) == 0:
        print("Did not find any frequent itemsets of length {}".format(k))
        sys.stdout.flush()
        break
    else:
        print("I found {} frequent itemsets of length {}".format(len(cur_frequent_itemsets), k))
        #print(cur_frequent_itemsets)
        sys.stdout.flush()
        frequent_itemsets[k] = cur_frequent_itemsets
# We aren't interested in the itemsets of length 1, so remove those
del frequent_itemsets[1]
print (frequent_itemsets[3])


candidate_rules = []
frequent_itemsets1=frequent_itemsets[3]
for itemset_length, itemset_counts in frequent_itemsets.items():
    if itemset_length>2:
        for itemset in itemset_counts.keys():
            for conclusion in itemset:
                premise = itemset - set((conclusion,))
                conclusionset = frozenset((conclusion,))
                candidate_rules.append((premise, conclusionset))
                candidate_rules.append((conclusionset,premise))
print("There are {} candidate rules".format(len(candidate_rules)))
print(candidate_rules)


correct_counts = defaultdict(int)
incorrect_counts = defaultdict(int)
for user, reviews in river_sp.items():
    for candidate_rule in candidate_rules:
        premise, conclusion = candidate_rule
        if premise.issubset(reviews):
            if conclusion.issubset(reviews):
                correct_counts[candidate_rule] += 1
            else:
                incorrect_counts[candidate_rule] += 1
rule_confidence = {candidate_rule: correct_counts[candidate_rule] / float(correct_counts[candidate_rule] + incorrect_counts[candidate_rule])
              for candidate_rule in candidate_rules}
              

min_confidence = 0.5
# Filter out the rules with poor confidence
rule_confidence = {rule: confidence for rule, confidence in rule_confidence.items() if confidence > min_confidence}
print(len(rule_confidence)) 

from operator import itemgetter
sorted_confidence = sorted(rule_confidence.items(), key=itemgetter(1), reverse=True)

for index in range(3):
    print("Rule #{0}".format(index + 1))
    (premise, conclusion) = sorted_confidence[index][0]
    print("Rule: If a person recommends {0} they will also recommend {1}".format(premise, conclusion))
    print(" - Confidence: {0:.3f}".format(rule_confidence[(premise, conclusion)]))
    print("")
