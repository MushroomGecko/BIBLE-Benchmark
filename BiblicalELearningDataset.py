import fitz  # PyMuPDF
import re
import json
import os
import string

bible_books = {
    "Genesis": "https://biblicalelearning.org/wp-content/uploads/2021/05/01_GenesisMCQuestions.pdf",
    "Exodus": "https://biblicalelearning.org/wp-content/uploads/2021/05/02_ExodusMCQuestions.pdf",
    "Leviticus": "https://biblicalelearning.org/wp-content/uploads/2021/05/03_LeviticusMCQuestions.pdf",
    "Numbers": "https://biblicalelearning.org/wp-content/uploads/2021/05/04_NumbersMCQuestions.pdf",
    "Deuteronomy": "https://biblicalelearning.org/wp-content/uploads/2021/05/05_DeutMCQuestions.pdf",
    "Joshua": "https://biblicalelearning.org/wp-content/uploads/2021/05/06_JoshuaMCQuestions.pdf",
    "Judges": "https://biblicalelearning.org/wp-content/uploads/2021/05/07_Judges_MCQuestions.pdf",
    "Judges_2": "https://biblicalelearning.org/wp-content/uploads/2021/05/07_GettingStartedWithJudges_MCQuestions_BeginOnly.pdf",
    "Ruth": "https://biblicalelearning.org/wp-content/uploads/2021/05/08_Ruth_MCQuestions.pdf",
    "1 Samuel": "https://biblicalelearning.org/wp-content/uploads/2021/05/09_Questions_1Samuel.pdf",
    "2 Samuel": "https://biblicalelearning.org/wp-content/uploads/2021/05/10_Questions_2Samuel.pdf",
    "1 Kings": "https://biblicalelearning.org/wp-content/uploads/2021/05/11_1Kings01_MCQuestions.pdf",
    "2 Kings": "https://biblicalelearning.org/wp-content/uploads/2021/05/12_2Kings_MCQuestions.pdf",
    "Ezra": "https://biblicalelearning.org/wp-content/uploads/2021/05/15_Ezra_MCQuestions.pdf",
    "Nehemiah": "https://biblicalelearning.org/wp-content/uploads/2021/05/16_Nehemiah_MCQuestions.pdf",
    "Esther": "https://biblicalelearning.org/wp-content/uploads/2021/05/17_Esther_MCQuestions.pdf",
    "Job": "https://biblicalelearning.org/wp-content/uploads/2021/05/18_Job_MCQuestions.pdf",
    "Psalms": "https://biblicalelearning.org/wp-content/uploads/2021/01/19_Psalms_Bible_Questions.pdf",
    "Proverbs": "https://biblicalelearning.org/wp-content/uploads/2021/05/20_ProverbsMCQuestions.pdf",
    "Ecclesiastes": "https://biblicalelearning.org/wp-content/uploads/2021/05/21_EcclesiastesMCQuestions.pdf",
    "Daniel": "https://biblicalelearning.org/wp-content/uploads/2021/05/27_Daniel_MCQuestions.pdf",
    "Hosea": "https://biblicalelearning.org/wp-content/uploads/2021/05/28_Hosea_MCQuestions.pdf",
    "Joel": "https://biblicalelearning.org/wp-content/uploads/2021/05/29_Joel_MCQuestions.pdf",
    "Amos": "https://biblicalelearning.org/wp-content/uploads/2021/05/30_Amos_MCQuestions.pdf",
    "Obadiah": "https://biblicalelearning.org/wp-content/uploads/2021/05/31_Obadiah_MCQuestions.pdf",
    "Jonah": "https://biblicalelearning.org/wp-content/uploads/2021/05/32_Jonah_MCQuestions.pdf",
    "Micah": "https://biblicalelearning.org/wp-content/uploads/2021/05/33_Micah_MCQuestions.pdf",
    "Nahum": "https://biblicalelearning.org/wp-content/uploads/2021/05/34_Nahum_MCQuestions.pdf",
    "Habakkuk": "https://biblicalelearning.org/wp-content/uploads/2021/05/35_Habakkuk_MCQuestions.pdf",
    "Zephaniah": "https://biblicalelearning.org/wp-content/uploads/2021/05/36_Zephaniah_MCQuestions.pdf",
    "Haggai": "https://biblicalelearning.org/wp-content/uploads/2021/05/37_Haggai_MCQuestions.pdf",
    "Malachi": "https://biblicalelearning.org/wp-content/uploads/2021/05/39_Malachi_MCQuestions.pdf",
    "Matthew": "https://biblicalelearning.org/wp-content/uploads/2023/04/01_Matthew_MCQuestions.pdf",
    "Mark": "https://biblicalelearning.org/wp-content/uploads/2023/04/02_Mark_MC_Questions.pdf",
    "Luke": "https://biblicalelearning.org/wp-content/uploads/2023/04/03_Luke_MC_Questions.pdf",
    "John": "https://biblicalelearning.org/wp-content/uploads/2023/04/04_John_MC_Questions.pdf",
    "Acts": "https://biblicalelearning.org/wp-content/uploads/2023/04/05_Acts_MC_Questions.pdf",
    "Romans": "https://biblicalelearning.org/wp-content/uploads/2023/04/06_Romans_MC_Questions.pdf",
    "1 Corinthians": "https://biblicalelearning.org/wp-content/uploads/2023/04/07_1Corinthians_MC_Questions.pdf",
    "2 Corinthians": "https://biblicalelearning.org/wp-content/uploads/2023/04/08_2Corinthians_MC_Questions.pdf",
    "Galatians": "https://biblicalelearning.org/wp-content/uploads/2023/12/09_Galatians_MC_Questions.pdf",
    "Ephesians": "https://biblicalelearning.org/wp-content/uploads/2023/04/10_Ephesians-Questions.pdf",
    "Philippians": "https://biblicalelearning.org/wp-content/uploads/2023/04/11_Philippians-Questions.pdf",
    "Colossians": "https://biblicalelearning.org/wp-content/uploads/2023/12/12_Colossians_Questions.pdf",
    "Revelation": "https://biblicalelearning.org/wp-content/uploads/2023/04/27_Revelation_MCQuestions.pdf"
}

alphabet = list(string.ascii_uppercase)

alphabet_to_index = {}
index_to_alphabet = {}

for value, index in enumerate(list(string.ascii_uppercase), start=0):
    alphabet_to_index[value] = index
    index_to_alphabet[index] = value

inch = 72
measure = inch * 0.75

def biblicalelearning_scraper(pdf):
    directory = "source_data/JSON/BiblicalELearning"
    os.makedirs(directory, exist_ok=True)
    with fitz.open(pdf) as data:
        is_question = False
        is_choice = False
        is_answer = False

        official_book_name = pdf.split("/")[1].split(".")[0].split("_")[0].strip()
        file_book_name = pdf.split("/")[1].split(".")[0].strip()

        local = {"question": "", "choice": [], "answer": ""}
        master = []

        for page in data.pages():
            page_data = page.get_text("blocks")
            top = measure
            bottom = page.rect.height - measure
            for chunk in page_data:
                if chunk[1] < top or chunk[3] > bottom:
                    continue
                paragraph = chunk[4].strip()
                if paragraph:
                    # print(paragraph)
                    for text in paragraph.split('\n'):
                        text = text.strip()
                        if text:
                            # print(text)
                            # Start of a question
                            if re.search(r'^\d+\.\s+', text) and is_question == False:
                                master.append(local)
                                # print(local)
                                local = {"question": "", "choice": [], "answer": "", "category": official_book_name, "source": bible_books[file_book_name]}
                                is_question = True
                                is_choice = False
                                is_answer = False
                                local["question"] += text + ' '
                            elif re.search(r'\s*?\d*?', text) and not (re.search(r'^[A-Za-z][a-z]?\.', text) or re.search(r'^[Α-Ω]\.', text)) and is_question == True:
                                is_question = True
                                is_choice = False
                                is_answer = False
                                local["question"] += text + ' '

                            # Answer choice
                            elif re.search(r'^[A-Za-z][a-z]?\.', text) or re.search(r'^[Α-Ω]\.', text):
                                is_question = False
                                is_choice = True
                                is_answer = False
                                local["choice"].append(text + ' ')
                            elif re.search(r'\s*?\d*?', text) and not (re.search(r'^[A-Za-z][a-z]?:', text) or re.search(r'^[A-Za-z];', text)) and is_choice == True:
                                is_question = False
                                is_choice = True
                                is_answer = False
                                local["choice"][-1] += text + ' '

                            # Answer
                            elif re.search(r'^[A-Za-z]:', text) or re.search(r'^[A-Za-z];', text):
                                is_question = False
                                is_choice = False
                                is_answer = True
                                local["answer"] += text + ' '
                            elif re.search(r'\s*?\d*?', text) and not re.search(r'^\d+\.\s+', text) and is_answer == True:
                                is_question = False
                                is_choice = False
                                is_answer = True
                                local["answer"] += text + ' '

        master.append(local)
    master.pop(0)
    final_master = []
    for item in range(len(master)):
        is_valid = True
        # print(master[item])
        if re.search(r'^\d+\.', master[item]["question"]):
            master[item]["question"] = master[item]["question"][re.search(r'^\d+\.', master[item]["question"]).end():]
        master[item]["question"] = master[item]["question"].strip()
        if not master[item]["question"]:
            # print(f"Book {pdf}. Blank Question: '{master[item]["question"]}'")
            is_valid = False

        for choice in range(len(master[item]["choice"])):
            master[item]["choice"][choice] = master[item]["choice"][choice].strip()[master[item]["choice"][choice].find('.')+1:].strip()
            if not master[item]["choice"][choice]:
                # print(master[item]["question"])
                # print(f"Book {pdf}. Blank Choice: '{master[item]["choice"][choice]}'")
                is_valid = False
                break

        master[item]["answer"] = master[item]["answer"].strip()
        if master[item]["answer"]:
            master[item]["answer"] = master[item]["answer"][0].strip()
        else:
            # print(master[item]["question"])
            # print(f"Book {pdf}. Blank Answer: '{master[item]["answer"]}'")
            is_valid = False
        if is_valid and len(master[item]["answer"]) != 1:
            # print(master[item]["question"])
            # print(f"Book {pdf}. Wrong Answer: '{master[item]["answer"]}'")
            is_valid = False
        if len(master[item]["answer"]) > 0 and not re.search(r'[A-Z]', master[item]["answer"]):
            # print(master[item]["question"])
            # print(f"Book {pdf}. Invalid Answer: '{master[item]["answer"]}'")
            is_valid = False

        try:
            options = alphabet.index(master[item]["answer"])
        except Exception as e:
            options = -1

        if (options + 1) > len(master[item]["choice"]) or options < 0:
            print(master[item]["question"])
            print(f"Book {pdf}. Invalid Answer: '{master[item]["answer"]}'")
            print(f"Choices: {master[item]["choice"]}")
            print()
            is_valid = False

        if is_valid:
            # print(master[item])
            master[item]["qa_extraction"] = f"Obtained directly from the source."
            final_master.append(master[item])

    print(f'Length of {pdf.split("/")[1].split(".")[0]}: {len(final_master)}')
    with open(f"{directory}/{file_book_name}.json", 'w') as local_write:
        json.dump(final_master, local_write, indent=4, ensure_ascii=False)

    return final_master

for book in os.listdir("source_data/BiblicalELearningPDFs"):
    scraped = biblicalelearning_scraper(f'source_data/BiblicalELearningPDFs/{book}')
