import json
import os
from collections import OrderedDict

directories = ["source_data/JSON/BiblicalELearning", "source_data/JSON/NotebookLM2"]
output = {}

for website in directories:
    for book in os.listdir(website):
        with open(f"{website}/{book}", "r") as file:
            json_obj = json.load(file)
            if json_obj[0]["category"] not in output:
                output[json_obj[0]["category"]] = []
            for obj in json_obj:
                choice_arr = []
                for choice in obj['choice']:
                    choice_arr.append(choice.strip())

                output[obj["category"]].append({'question': obj['question'].strip(),
                                                'choices': choice_arr,
                                                'answer': obj['answer'].strip(),
                                                'category': obj['category'].strip(),
                                                'source': obj['source'].strip(),
                                                'qa_extraction': obj['qa_extraction'].strip()})

output = dict(sorted(output.items()))
print(output.keys())

if output:
    print(f'Number of categories in Bible Benchmark dataset: {len(output)}')
    counter = 0
    for category in output:
        counter += len(output[category])
    print(f'Number of questions in Bible Benchmark dataset: {counter}')
    with open(f"final.json",'w') as local_write:
        json.dump(output, local_write, indent=4, ensure_ascii=False)
else:
    print("No information found.")