# BIBLE-Benchmark: Data Collection & Transformation

**BIBLE** (Biblically Informed Bot Learning Evaluation) is a comprehensive **benchmark dataset** designed to **evaluate** AI models on their understanding of the Holy Bible. This repository contains the source code and data collection pipeline for building the dataset—it is intended for **transparency and reproducibility** of the data transformation process.

> ℹ️ **Dataset Repository**: The actual benchmark dataset is published on [HuggingFace](https://huggingface.co/datasets/MushroomGecko/BIBLE). This repository documents how the data was collected and processed.

---

## 🚀 Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MushroomGecko/BIBLE-Benchmark.git
cd BIBLE-Benchmark
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. For benchmarking with Ollama, ensure [Ollama](https://ollama.ai/) is installed and running on your system.

---

## ⚠️ Accuracy Disclaimer

While the questions in this dataset are sourced directly from trusted materials, a significant portion of the content was generated using **NotebookLM** based on the referenced source documents. Many of these generated questions and answers were not manually reviewed for theological or factual accuracy.

As such, **the accuracy, phrasing, and interpretative correctness of some questions and answers cannot be guaranteed**. Users are encouraged to independently verify any content used in formal evaluations, especially in faith-sensitive or doctrinally rigorous contexts.

---

## 📚 Dataset Overview

The BIBLE dataset includes:
- ✅ Questions from every book of the Bible (Genesis → Revelation)
- ✅ Additional themed categories:
  - **People of the Bible**
  - **Places in the Bible**
  - **Measurements in the Bible**
- ✅ Structured format with:
  - Multiple-choice options (A–D)
  - A single correct answer
  - Source attribution and extraction method
- ✅ Suitable for:
  - Benchmarking model comprehension of Scripture
  - Evaluating closed-book Biblical knowledge in LLMs
  - Faith-aligned QA assessments

---

## 📊 Dataset Structure

Each example in the dataset is a dictionary with the following fields:

- `question`: A Bible-based question
- `choices`: A list of four possible answers (A–D)
- `answer`: The correct choice, as a letter ("A", "B", "C", or "D")
- `category`: The book of the Bible or theme the question belongs to
- `source`: A URL pointing to the original source material
- `qa_extraction`: Notes on how the question-answer pair was derived (e.g., "Obtained directly from the source" or "Generated via NotebookLM from the source")

### 🔍 Example

```json
{
  "question": "What two things did God create in the beginning (Gen. 1:1)?",
  "choices": [
    "The light and the darkness",
    "The heavens and the earth",
    "The land and the sea",
    "The world and the stars"
  ],
  "answer": "B",
  "category": "Genesis",
  "source": "https://biblicalelearning.org/wp-content/uploads/2021/05/01_GenesisMCQuestions.pdf",
  "qa_extraction": "Obtained directly from the source."
}
```

---

## 📁 Data Pipeline & Directory Structure

### Source Data (`source_data/`)
- **BiblicalELearningPDFs/**: PDFs from Biblical eLearning that are parsed and formatted into the benchmark
- **GotQuestionsScrapes/**: Scrapes from GotQuestions Ministries that are passed into NotebookLM to generate people, places, and measurements data
  - `measurements/`: PDF representations of measurement data
  - `people/`: PDF representations of people data
  - `places/`: PDF representations of places data
- **JSON/**: Intermediate JSON representations during processing
  - `BiblicalELearning/`: JSON representation of the PDFs from `BiblicalELearningPDFs/`
  - `NotebookLM/`: Raw, semi-reviewed AI-generated content from NotebookLM, created by manually pasting Bible books from the WEB bible and GotQuestions Ministries PDFs (scraped by scripts in this repo) into the tool.
  - `NotebookLM2/`: Transformed versions of the data in `NotebookLM/` to fit the final data schema

### Output Data
- **final.json**: The combined and normalized data from all sources
- **HuggingFace/**: Parquet format representation of `final.json`, split by category (one subdirectory per Bible book and theme)

---

## 🔧 Data Transformation Scripts

The following scripts handle the data pipeline in sequence:

1. **GotQuestionsScraperMeasurements.py**: Scrapes measurement data from GotQuestions Ministries and saves as PDFs in `source_data/GotQuestionsScrapes/measurements`
2. **GotQuestionsScraperPeople.py**: Scrapes people data from GotQuestions Ministries and saves as PDFs in `source_data/GotQuestionsScrapes/people`
3. **GotQuestionsScraperPlaces.py**: Scrapes places data from GotQuestions Ministries and saves as PDFs in `source_data/GotQuestionsScrapes/places`
4. **BiblicalELearningDataset.py**: Parses PDFs from `source_data/BiblicalELearningPDFs` and converts them to JSON in `source_data/JSON/BiblicalELearning`
5. **NotebookLMDataset.py**: Transforms raw NotebookLM data from `source_data/JSON/NotebookLM` into normalized format in `source_data/JSON/NotebookLM2`
6. **DatasetCombiner.py**: Combines and normalizes data from `source_data/JSON/NotebookLM2` and `source_data/JSON/BiblicalELearning` into `final.json`
7. **HuggingFaceDataTransformer.py**: Converts `final.json` into Parquet format and stores it in the `HuggingFace/` directory, split by category

---

## 📝 Prompt Templates

Two prompt templates are used to generate questions via **NotebookLM**. They are located in the `prompts/` directory:

### PromptVerse.txt

Used for Bible books and categories with verse references.

**Key Features:**
- Instructs NotebookLM to generate 25 multiple-choice questions per input
- Requires questions to **reference Bible verse(s)** they are derived from (e.g., "1 Kings 1:1")
- Specifies JSON schema format for output consistency
- Ensures randomized answer positioning to avoid predictable patterns
- Requires balanced distribution of correct answers (A, B, C, D equally)
- Includes copyright protection guidance for generated content
- No bolded text in questions

**Usage:**
Used when generating questions for Bible books and topics with specific scripture references.

### PromptNoVerse.txt

Used for measurement-based categories without explicit verse references.

**Key Features:**
- Instructs NotebookLM to generate 25 multiple-choice questions per input
- Focuses on biblical **units of weight, length, volume, or currency**
- Does NOT require explicit Bible verse references in questions
- Questions must cite the PDF they originate from
- Specifies JSON schema format for output consistency
- Ensures randomized answer positioning to avoid predictable patterns
- Requires balanced distribution of correct answers (A, B, C, D equally)
- Includes copyright protection guidance for generated content

**Usage:**
Used when generating questions for categories like Measurements that don't have verse-specific content.

**Output Location:**
The output from NotebookLM following either prompt is stored in `source_data/JSON/NotebookLM/` before being transformed by `NotebookLMDataset.py`.

---

## 🧪 Benchmarking & Evaluation

### Benchmark.py

This script evaluates AI models on the BIBLE benchmark dataset using the [Ollama](https://ollama.ai/) framework.

**Features:**
- Tests models against all questions in `final.json`
- Supports multiple models (configurable via model variable)
- Records accuracy, adherence to instructions, and timing metrics
- Outputs detailed results to `Results/` directory as JSON

**Metrics Tracked:**
- `percent_correct`: Overall accuracy percentage
- `percent_obeyed`: Percentage of responses that followed the single-letter-only instruction
- `average_time`: Average time per question
- Per-question results including model response, correctness, and instruction adherence

**Usage:**
1. Ensure Ollama is installed and running
2. Select the model to test by uncommenting one of the model lines
3. Run: `python Benchmark.py`
4. Results will be saved to `Results/{model_name}.json`

**Output (`Results/` Directory):**
Each benchmark run produces a JSON file named after the tested model. Each file contains:
- `category`: The Bible book or theme category
- `question`: The question asked
- `choices`: The multiple-choice options
- `model_response`: The model's response (processed and cleaned)
- `correct_answer`: The correct answer letter
- `is_correct`: Boolean indicating if the model answered correctly
- `did_obey`: Boolean indicating if the model followed the single-letter-only instruction
- `source`: The source URL of the question
- Summary statistics at the end:
  - `total_questions`: Total number of questions in the benchmark
  - `overall_correct`: Number of correct answers
  - `percent_correct`: Accuracy percentage
  - `overall_obeyed`: Number of responses that followed instructions
  - `percent_obeyed`: Instruction adherence percentage
  - `total_time`: Total execution time
  - `average_time`: Average time per question

**Models Tested:**
The script includes commented examples of various models that can be tested, including:
- Qwen3 series (0.6b, 1.7b, 4b variants)
- Gemma series (2b, 3b, 3n variants)
- Llama 3.2 (1b, 3b variants)
- Phi series (mini instruct)
- And more...

---

## 🔗 Data Sources and Attribution

This dataset was built from publicly available resources. Full respect and credit is given to the following original sources:

- **Biblical eLearning**  
  Developed by Dr. Ted Hildebrandt, [Biblical eLearning](https://biblicalelearning.org/) is dedicated to providing free online Biblical resources to the global Christian community. The site hosts high-quality, Biblically grounded materials from expert teachers, aiming to preserve and share faithful teaching digitally for the glory of God and the good of others. Many of these resources, including the Bible Quizzers material used in this dataset, are freely **downloadable** in PDF format for personal study or educational use.  
  📖 [Download Bible Quizzers PDFs](https://biblicalelearning.org/quizlet-bible-quizzers/)

- **World English Bible (WEB)** via **[eBible.org](https://ebible.org/)**  
  [eBible.org](https://ebible.org) is the original home of the World English Bible and a global volunteer movement committed to making the Holy Bible freely available in the languages and formats most useful to people worldwide. Founded by Michael Paul Johnson, who also serves as senior editor of the WEB, the site hosts hundreds of translations, including the original Hebrew and Greek texts, and supports a wide range of digital formats for both reading and development. The mission of eBible.org is rooted in the Great Commission and made possible by a large network of volunteers who work to ensure quality, accessibility, and faithful distribution of Scripture.  
  📖 [Download the WEB Bible PDFs](https://ebible.org/pdf/eng-web/)

- **GotQuestions Ministries**  
  [GotQuestions.org](https://www.gotquestions.org/)  
  A leading online ministry offering Biblical answers to spiritually related questions, GotQuestions.org is a theologically conservative, evangelical resource rooted in Scripture. Since 2002, the site has received over 2.5 billion pageviews, offering articles, Q&A, podcasts, and tools for those seeking to understand the Word of God.

Each question entry includes the corresponding source URL and method of extraction of the data.  
If you use this dataset, please ensure these sources are properly cited.

---

## 🔍 Intended Use

The BIBLE dataset is intended for:
- Evaluating **Biblical literacy** in large language models
- Testing for **factual Scriptural grounding**
- Benchmarking theological comprehension
- Identifying hallucination in religious QA settings

It is **not suitable for model training**, and it is recommended that models be evaluated "as-is" without memorization or prior exposure to the benchmark.

---

## ⚖️ License

This repository and all data transformation scripts are released under the **GNU General Public License v3.0 (GPL-3.0)**.

The dataset itself (published on HuggingFace) is released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. It contains public domain and freely licensed material, but users are responsible for proper attribution and for complying with the original source usage guidelines.

---

## 🤝 Contributing

Found an issue or want to contribute additional benchmark questions?  
Pull requests and community suggestions are welcome — feel free to open an issue or submit a PR.

---

## 📝 Citation

If you use the BIBLE dataset in your research, please cite it appropriately and ensure proper attribution to the original sources listed above.
