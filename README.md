
# AI-Assisted Side-Channel Attacks

**Thesis Project by Miroslav Todorović**

Master's Thesis
Slovak Technical University, Faculty of Informatics and Information Technology
Bratislava

---

## 📚 Overview

This project uses Artificial Intelligence techniques, particularly deep learning models, to perform side-channel attacks on cryptographic implementations. The goal is to demonstrate how AI can enhance the efficiency and accuracy of these attacks by learning patterns from physical leakage data on power traces.

---

## 🧠 AI & Model Details

The model is implemented using:
- **TensorFlow / Keras** for the CNN architecture
- **Scikit-learn** for preprocessing and splitting the dataset
- **NumPy / Pandas** for data handling
- **Matplotlib** for visualizations
- **Wandb** for logging model stats and artifacts
---

## 🗃️ Dataset

> ⚠️ The datasets are large to be included in this repository.
To use the project, please download the dataset from [REPOSITORY](https://github.com/XIAOLUHOU/SCA-measurements-and-analysis----Experimental-results-for-textbook/tree/main) and place the datasets in the `datasets/` folder.

Datasets used:
- random_dataset,
- random_pt_dataset,
- fixed_dataset_1,
- fixed_dataset_2
---

## ⚙️ Wandb Logging

I've setup a logging with Wandb so the model artifacts are uploaded to it with the metrics. To use it create an **.env** file and add you API Wandb key in format: **WANDB_API_KEY=........**.

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/xtodorovic/your-repo-name.git
cd your-repo-name
```

### 2. Create and Activate Virtual Environment

#### On macOS/Linux:

```bash
./setup_env.sh
```

#### On Windows:

```cmd
setup_env.bat
```

This script will:
- Create a Python virtual environment
- Activate it
- Install all required dependencies (including Jupyter support) - It may show errors if there are some, follow given instructions

---

### 3. Open the Notebook in VSCode

Make sure you have the **Python** and **Jupyter** extensions installed.  
Then:
- Open the `.ipynb` file
- Click the top-right corner kernel selector
- Choose: `Python 3.x ('venv': venv)`

---

## 📦 Dependencies

See `requirements.txt` for a full list of required packages.

---

## 📦 Table of Contents

- **model/** - directory for model training and tuning
- **research** - contains research of the trace leakeages for both AES and PRESENT
- **utils** - contains helper functions (eg. dataset loader, computations, analasys methods...)

---

## 📄 License

This code is intended for academic and research purposes only.  
Please cite or reference appropriately if you use or modify this work.
