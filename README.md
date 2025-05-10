# AI-Assisted Side-Channel Attacks

**Master's Thesis Project**

**Author:** Bc. Miroslav Todorović

**Supervisor:** Bc. Xiaolu Hou, Ph.D.

**Institution:** Slovak Technical University, Faculty of Informatics and Information Technology, Bratislava

---

## 📖 Overview

This project explores the application of **Artificial Intelligence**—particularly **Convolutional Neural Networks (CNNs)**—in conducting **Side-Channel Attacks (SCAs)** on cryptographic implementations for **PRESENT** and **AES** ciphers. The aim is to enhance key recovery through machine learning models trained on power consumption traces during encryption.

---

## 🧠 AI & Model Framework

Key components and libraries used:

- `TensorFlow` / `Keras` – Model development and training (CNN architecture)
- `Scikit-learn` – Data splitting, scaling, preprocessing
- `NumPy`, `Pandas` – Data handling
- `Matplotlib` – Visualization
- `Weights & Biases (wandb)` – Experiment tracking and model artifact logging

---

## 📁 Dataset

> ⚠️ **Note:** Datasets are large and not hosted in this repository.  
Download them from:  
🔗 [Dataset Repository](https://github.com/XIAOLUHOU/SCA-measurements-and-analysis----Experimental-results-for-textbook/tree/main)

Expected datasets structure:

```
datasets/
├── random_dataset/
├── random_pt_dataset/
├── fixed_dataset_1/
└── fixed_dataset_2/
```

Each dataset contains traces and plaintexts. **random_dataset** also contains keys and it will serve as a training dataset.
Other datasets are for testing, and their true key is **FEDCBA0123456789**.

---

## 📊 Wandb Logging

This project supports Wandb for metrics tracking. To enable:

1. Create a `.env` file in the root folder.
2. Add your Wandb API key:

```env
WANDB_API_KEY=your_key_here
```

In case you don't want to track the metrics, comment out or delete the lines where wandb is used.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/xtodorovic/ing-thesis.git
cd ing-thesis
```

### 2. Set Up the Environment

#### On Linux/macOS:

```bash
./setup_env.sh
```

#### On Windows:

```cmd
setup_env.bat
```

This script:
- Creates a virtual environment
- Installs dependencies (including Jupyter support)
- Prepares the environment for trace-based model training

Script is not perfect and may fail if you don't have python installed. I used it so I can activate the env quickly.

---

## 🧪 Running the Jupyter Notebooks

1. Launch VSCode.
2. Open any `.ipynb` file (e.g., `train.ipynb`).
3. In the top-right kernel selector, pick the Python interpreter from the `venv`.

---

## 📦 Dependencies

See `requirements.txt` for all required packages.

---

## 🗂️ Project Structure

High-level module structure and tree outlines are in:

- [`main.txt`](tree/main.txt)
- [`datasets.txt`](tree/datasets.txt)
- [`prepared_dataset.txt`](tree/prepared_data.txt)
- [`trained_models.txt`](tree/trained_models.txt)
- [`tuner_search_hp.txt`](tree/tuner_search_hp.txt)

Project Layout:

```text
.
├── datasets_URL.txt
├── datasets - Training and testing datasets
├── dataset - Training data with labels and POIs
├── model
│   ├── key_recovery.ipynb - Notebook for evaluation of trained models and key recovery
│   ├── train.ipynb - Notebook for model training
│   └── tunning.ipynb - Notebook for hyperparameter search using keras tuner
├── prototype.ipynb - Initial prototype of the project
├── README.md 
├── requirements.txt - Dependencies list
├── research - Directory for researching, ploting and exporting leakage POIs
│   ├── trace_research_AES.ipynb 
│   └── trace_research_PRESENT.ipynb
├── setup_env.bat - File to make a virtual env, install dependencies and activate it for Windows
├── setup_env.sh -  File to make a virtual env, install dependencies and activate it for Linux/macOS
├── tree - Directory containing tree structure of the project
│   ├── main.txt
│   ├── prepared_data.txt
│   ├── project_tree.txt
│   └── trained_models.txt
└── utils 
    ├── analysis.py - Module for analysis methods
    ├── compute.py - Module for cumpute methods such as compute SBox for PRESENT and AES 
    ├── dataset_loader.py - Module for easier dataset loading
    ├── __init__.py - Empty file, created so the interpreter knows to locate modules in this dir for reusability
    ├── my_model.py - Contains 2 CNN models, one for POI training and one for Ranged POI 
    └── tuner_models.py - Different models that were created so that the tuner may find good hyperparameters

5 directories, 22 files

```

---

## 📜 License

This project is for academic and research purposes.
Please cite appropriately if used in publications or further work.