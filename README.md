# GoIT Computer Science Homework 05

This repository contains solutions for two tasks related to file processing and text analysis.

## Prerequisites

To run both scripts, you need to set up a virtual environment and install the dependencies.

1.  **Create and activate a virtual environment:**

    ```bash
    # Create the environment
    python3 -m venv .venv
    
    # Activate on Linux/macOS
    source .venv/bin/activate
    
    # Activate on Windows (PowerShell)
    # .\.venv\Scripts\Activate.ps1
    ```

2.  **Install the required libraries:**

    ```bash
    pip install -r requirements.txt
    ```

---

## Task 1: Asynchronous File Sorting

The `task1/main.py` script recursively reads files in a source folder and asynchronously copies them to a destination folder, sorting them into subfolders based on file extension.

### Usage

To run the script, use the following command, specifying the source folder and, optionally, the destination folder.

```bash
python task1/main.py --source <path_to_source_folder> --output <path_to_destination_folder>
```

- `--source`: **(Required)** The path to the folder with files to be sorted.
- `--output`: (Optional) The path to the folder where the sorted files will be copied. Defaults to `dist`.

**Example:**

```bash
python task1/main.py --source ./source_folder --output ./sorted_files
```

---

## Task 2: Word Frequency Analysis using MapReduce

The `task2/main.py` script downloads text from a given URL, analyzes word frequency using a multi-threaded implementation of the MapReduce paradigm, and saves a visualization of the top 15 most frequent words as a chart.

### Usage

To run the script, execute:

```bash
python task2/main.py
```

### Result

The script will automatically download the text "A Shevchenko Anthology" from Project Gutenberg. After the analysis is complete, a file named `word_frequency.png` will be created in the `task2/` folder, containing a chart of the most popular words.

You can change the URL inside the `task2/main.py` file to analyze any other text.