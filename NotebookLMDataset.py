import json
import os

book_links = {"1 Chronicles": "https://ebible.org/pdf/eng-web/eng-web_1CH.pdf",
              "2 Chronicles": "https://ebible.org/pdf/eng-web/eng-web_2CH.pdf",
              "Song of Solomon": "https://ebible.org/pdf/eng-web/eng-web_SNG.pdf",
              "Isaiah": "https://ebible.org/pdf/eng-web/eng-web_ISA.pdf",
              "Jeremiah": "https://ebible.org/pdf/eng-web/eng-web_JER.pdf",
              "Lamentations": "https://ebible.org/pdf/eng-web/eng-web_LAM.pdf",
              "Ezekiel": "https://ebible.org/pdf/eng-web/eng-web_EZK.pdf",
              "Zechariah": "https://ebible.org/pdf/eng-web/eng-web_ZEC.pdf",
              "1 Thessalonians": "https://ebible.org/pdf/eng-web/eng-web_1TH.pdf",
              "2 Thessalonians": "https://ebible.org/pdf/eng-web/eng-web_2TH.pdf",
              "1 Timothy": "https://ebible.org/pdf/eng-web/eng-web_1TI.pdf",
              "2 Timothy": "https://ebible.org/pdf/eng-web/eng-web_2TI.pdf",
              "Titus": "https://ebible.org/pdf/eng-web/eng-web_TIT.pdf",
              "Philemon": "https://ebible.org/pdf/eng-web/eng-web_PHM.pdf",
              "Hebrews": "https://ebible.org/pdf/eng-web/eng-web_HEB.pdf",
              "James": "https://ebible.org/pdf/eng-web/eng-web_JAS.pdf",
              "1 Peter": "https://ebible.org/pdf/eng-web/eng-web_1PE.pdf",
              "2 Peter": "https://ebible.org/pdf/eng-web/eng-web_2PE.pdf",
              "1 John": "https://ebible.org/pdf/eng-web/eng-web_1JN.pdf",
              "2 John": "https://ebible.org/pdf/eng-web/eng-web_2JN.pdf",
              "3 John": "https://ebible.org/pdf/eng-web/eng-web_3JN.pdf",
              "Jude": "https://ebible.org/pdf/eng-web/eng-web_JUD.pdf",
              "People": "https://www.gotquestions.org/content_people.html",
              "Places": "https://www.gotquestions.org/questions_Bible-places.html",
              "Measurements": "https://www.gotquestions.org/biblical-weights-and-measures.html"
              }

overall = 0
for book in os.listdir('source_data/JSON/NotebookLM'):
    book_list = []
    if '.json' in book:
        with open(f"source_data/JSON/NotebookLM/{book}", "r", encoding='utf-8') as file:
                json_obj = json.load(file)
                for data_point in json_obj:
                    if "question" not in data_point or "choice" not in data_point or "answer" not in data_point:
                        print(f"Book {book} has bad item: {data_point}")
                    else:
                        data_point["category"] = book.split('.')[0].strip()
                        if book != 'People.json' and book != 'Places.json':
                            data_point["source"] = f"{book_links[book.split('.')[0]].strip()}"
                        else:
                            data_point["source"] = f"https://www.gotquestions.org/{data_point["source"].replace('.pdf', '').strip()}"
                        data_point["qa_extraction"] = f"Generated via NotebookLM given the source."

                        book_list.append(data_point)
                print(f"{book.replace('.json', '')}: {len(json_obj)}")
                overall += len(json_obj)
                with open(f"source_data/JSON/NotebookLM2/{book}", "w", encoding='utf-8') as file_out:
                    json.dump(book_list, file_out, indent=4, ensure_ascii=False)
print(f"Overall: {overall}")
