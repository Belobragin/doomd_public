from nfateev import train_corpus_full

temp_arr = train_corpus_full['intents']
dialog = []
#print(temp_arr)
# with open('nfateev_corpus.py', 'w') as ff:
#     for i, dialog_dict in enumerate(temp_arr):
#         temp_patterns = temp_arr[i]['patterns']
#         temp_responses = temp_arr[i]['responses']
#         for k in range(len(temp_patterns)):
#             for h in range(len(temp_responses)):
#                 tag_pattern = temp_patterns[k]
#                 #tag_response = temp_responses[k]
#                 #dialog.extend([tag_pattern, temp_responses[h]] for h in range(len(temp_responses)))
#                 dialog.append(tag_pattern)
#                 dialog.append(temp_responses[h])
#     print(len(dialog))
#     ff.write('train_corpus_full = ')
#     ff.write(str(dialog)) 

with open('nfateev_corpus1.py', 'w') as ff:
    for i, dialog_dict in enumerate(temp_arr):
        temp_patterns = temp_arr[i]['patterns']
        temp_responses = temp_arr[i]['responses']
        for k in range(len(temp_patterns)):
            tag_pattern = temp_patterns[k]
                #tag_response = temp_responses[k]
            dialog.extend([tag_pattern, temp_responses[h]] for h in range(len(temp_responses)))
                #dialog.append(tag_pattern)
                #dialog.append(temp_responses[h])
    print(len(dialog))
    ff.write('train_corpus_full = ')
    ff.write(str(dialog))     
