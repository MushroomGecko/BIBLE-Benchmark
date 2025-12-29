from datetime import datetime
import json
import ollama
from llama_cpp import Llama
import re
import string
import time

### OLLAMA MODELS ###
# model = "gemma3:1b"
# model = "granite3.1-moe:1b-instruct-q4_K_M"
# model = "llama3.2:1b-instruct-q4_K_M"
# model = "deepseek-r1:1.5b-qwen-distill-q4_K_M"
# model = "qwen2.5:1.5b-instruct-q4_K_M"
# model = "qwen3:0.6b-q4_K_M"
# model = "qwen3:1.7b-q4_K_M"
# model = "qwen3:4b-q4_K_M"
# model = "qwen3:4b-instruct-2507-q4_K_M"
# model = "smollm2:1.7b-instruct-q4_K_M"
# model = "internlm2:1.8b-chat-v2.5-q4_K_M"
# model = "gemma2:2b-instruct-q4_K_M"
# model = "granite3.1-dense:2b-instruct-q4_K_M"
# model = "granite3.2:2b-instruct-q4_K_M"
# model = "hermes3:3b"
# model = "llama3.2:3b-instruct-q4_K_M"
# model = "qwen2.5:3b-instruct-q4_K_M"
# model = "hf.co/bartowski/Phi-3.5-mini-instruct-GGUF:Q4_K_M"
# model = "hf.co/unsloth/Phi-4-mini-instruct-GGUF:Q4_K_M"
# model = "cogito:3b-v1-preview-llama-q4_K_M"
# model = "gemma3:4b"
model = "gemma3n:e2b-it-q4_K_M"

### LLAMA CPP MODELS ###
model = {"repo_id": "LiquidAI/LFM2-2.6B-Exp-GGUF", "filename": "LFM2-2.6B-Exp-Q4_K_M.gguf"}

# If Qwen3 (not the Thinking ot Instruct variant) is the model being tested, set to `/think` for thinking or `/no_think` to turn thinking off
think_enable = ""

# Choose the runner
# runner = "ollama"
runner = "llama_cpp"

def generate_ollama(model, user_prompt, system_prompt):
    return ollama.generate(model=model,
                           prompt=user_prompt,
                           system=system_prompt,
                           keep_alive=-1)["response"]

def generate_llama_cpp(llm, model, user_prompt, system_prompt):
    response = llm.create_chat_completion(
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )
    return response["choices"][0]["message"]["content"]

if runner == "llama_cpp":
    llm = Llama.from_pretrained(
        repo_id=model["repo_id"],
        filename=model["filename"],
        )
else:
    llm = None

alphabet_to_index = {}
index_to_alphabet = {}

for index, value in enumerate(list(string.ascii_uppercase), start=0):
    alphabet_to_index[value] = index
    index_to_alphabet[index] = value

question_len = 0
correct = 0
obeyed = 0
final_output = []
with open('final.json', 'r', encoding='utf-8') as file:
    json_obj = json.load(file)
    # json_obj = {'People': json_obj['People']}
    for i in json_obj:
        question_len += len(json_obj[i])
    print(question_len)
    time_counter = 1
    start_time = time.time()
    for category in json_obj:
        for data in json_obj[category]:
            letters = []
            for letter in range(len(data['choices'])):
                letters.append(index_to_alphabet[letter])

            system_prompt = (f"You are an AI expert in the Holy Bible.\n"
                             f"You excel at multiple-choice Bible quizzes and exams.\n"
                             f"For each question, analyze the given choices and respond with only the letter corresponding to the correct answer.\n"
                             f"The available answer choices are: {', '.join(letters)}.\n"
                             f"Respond with a single letter only, without explanations, extra text, or punctuation.\n"
                             f"If uncertain, choose the best answer based on biblical knowledge.\n"
                             f"Strictly follow these rules, or your response will be considered incorrect.")

            choice_string = ""
            for choice in range(len(data['choices'])):
                choice_string += f"\t{index_to_alphabet[choice]}) {data['choices'][choice]}\n"

            user_prompt = (f"### INSTRUCTION ###\n"
                           f"Select the correct answer from the choices below. Respond with only one of the corresponding letters: {', '.join(letters)}.\n"
                           f"\n"
                           f"### QUESTION ###\n"
                           f"{data['question']}\n"
                           f"{choice_string}\n"
                           f"Provide only the letter corresponding to the correct answer.{think_enable}")

            if runner == "ollama":
                response = generate_ollama(model, user_prompt, system_prompt)
            elif runner == "llama_cpp":
                response = generate_llama_cpp(llm, model, user_prompt, system_prompt)

            think_tag = '</think>'
            if think_tag in response:
                response = response[response.find(think_tag) + len(think_tag) + 1:].strip()

            cleaned_response = response.translate(str.maketrans('', '', string.punctuation)).upper().replace('\n', ' ').strip()
            cleaned_answer = data['answer'].translate(str.maketrans('', '', string.punctuation)).upper().strip()
            # print(cleaned_answer)

            is_correct = False
            did_obey = False
            if cleaned_response == cleaned_answer:
                correct += 1
                is_correct = True
            else:
                reg_response = re.findall(r' [A-Z] ', f" {cleaned_response} ")
                if reg_response and len(reg_response) == 1 and reg_response[0] == cleaned_answer:
                    correct += 1
                    is_correct = True

            if len(cleaned_response.split()) == 1:
                obeyed += 1
                did_obey = True

            final_output.append({'category': data['category'],
                                 'question': data['question'],
                                 'choices': data['choices'],
                                 'model_response': cleaned_response,
                                 'correct_answer': data['answer'],
                                 'is_correct': is_correct,
                                 'did_obey': did_obey,
                                 'source': data['source']})
            """
            print(f"Question      : {data['question']}")
            print(f"Choices       : {data['choices']}")
            print(f"Model Response: {cleaned_response}")
            print(f"Correct Answer: {data['answer']}")
            print(f"Is Correct    : {is_correct}")
            print(f"Did Obey      : {did_obey}")
            """
            print(f"Completed: {time_counter}/{question_len}, Time Remaining: {((time.time() - start_time) / time_counter) * (question_len - time_counter)}, Time: {datetime.now()}, Correct: {is_correct}")
            time_counter += 1

final_output.append({'total_questions': question_len,
                     'overall_correct': correct,
                     'percent_correct': (correct / question_len) * 100,
                     'overall_obeyed': obeyed,
                     'percent_obeyed': (obeyed / question_len) * 100,
                     'total_time': (time.time() - start_time),
                     'average_time': (time.time() - start_time) / question_len})
print()
print(f"Overall Correct: {correct}/{question_len}")
print(f"Percent Correct: {(correct / question_len) * 100}%")
print(f"Overall Obeyed: {obeyed}/{question_len}")
print(f"Percent Obeyed: {(obeyed / question_len) * 100}%")
print(f"Total Time: {(time.time() - start_time)}")
print(f"Average Time: {(time.time() - start_time) / question_len}")

with open(f'Results/{model.replace(':', '_').replace('.', '_').replace('-', '_').replace('/', '_').strip()}.json', 'w', encoding='utf-8') as fileout:
    json.dump(final_output, fileout, indent=4, ensure_ascii=False)
