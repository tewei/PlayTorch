import csv
import re
from collections import defaultdict
import dialog_config
from nltk import word_tokenize

raw_data = []
with open('data/restaurant_clean.tsv') as csvfile:
    rdr = csv.reader(csvfile, delimiter='\t')
    next(rdr)
    for row in rdr:
        #print (row)
        raw_data.append([int(row[0]), int(row[1]), row[3], row[4], row[5:]])

def get_intent_slot_pairs(raw_list):
    intent_slot_pair = []
    for intent_slots in raw_list:
        if intent_slots != '':
            try:
                intent = re.split('([_a-zA-Z]*)\((.*)\)', intent_slots, 1)[1]
                slots_str = re.split(';\s*', re.split('[_a-zA-Z]*\((.*)\)\s*$', intent_slots, 1)[1])
            except:
                print ('failed: ' + intent_slots)
            for s in slots_str:
                intent_slot_pair.append((intent, s.split('=')[0]))
                #print(intent, s.split('=')[0])
    
    return intent_slot_pair

def clean_data():
    label_cnt = defaultdict(int)
    label_idx = {}
    label_list = []
    real_data = []
    
    for row in raw_data:
        pairs = get_intent_slot_pairs(row[4])
        row_labels = []
        for p in pairs:
            if(p[1] != ''):
                label_name = p[0]+'_'+p[1]
            else:
                label_name = p[0]

            label_name = label_name.lower()
            if len(label_name) > 50:
                continue
            if(label_cnt[label_name] == 0):
                label_list.append(label_name)
            label_cnt[label_name] += 1
            if label_name not in row_labels:
                row_labels.append(label_name)
        
        row_labels.sort()
        sent_tok = word_tokenize(row[3])
        if len(sent_tok) > 0 and len(row_labels) > 0:
            real_data.append((sent_tok, row_labels))
    
    label_list.sort()
    for i, l in enumerate(label_list):
        label_idx[l] = i

    return label_idx, label_list, label_cnt, real_data

label_idx, label_list, label_cnt, real_data = clean_data()

label_list.sort()
for i, label in enumerate(label_list):
    label_idx[label] = i
    print (i, label, label_cnt[label])

#print(real_data[0:10])