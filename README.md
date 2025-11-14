
# Fine-tuning Whisper for Non-Standard Kenyan English and Swahili 🇰🇪

![In Progress](https://img.shields.io/badge/Status-In%20Progress-green?style=for-the-badge&logo=wrench&logoColor=white)

[![Hugging Face Models](https://img.shields.io/badge/Hugging%20Face-smainye%2Fmodels-yellow?logo=huggingface)](https://huggingface.co/smainye/models)



This project is dedicated to fine-tuning, evaluating, and running inference on non-standard speech datasets for Kenyan English and Swahili on open ai whisper-tiny, whisper-small & whisper-large-v3 models.The primary goal is to develop a fine-tuned model that better understands non-standard speech for Kenyan English and Swahili, achieving a lower Character Error Rate (CER) and Word Error Rate (WER).

---

## Associated Organisations 🤝

This project is associated with the following **partner organisations**:

* [Centre for Digital Language Inclusion](https://cdl-inclusion.com/) 🌐
* [Senses Hub](https://senseshub.vision/) 🇰🇪
* [iLabAfrica at Strathmore University](https://ilabafrica.strathmore.edu/) 🇰🇪
* [University College London](https://www.ucl.ac.uk/) 🇬🇧
* [Global Disability Innovation Hub](https://www.disabilityinnovation.com/) 🇬🇧


---

# Technology Stack 🛠️

| Category | Technologies |
| :--- | :--- |
| **Language** | [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)|
| **Data & Models** | [![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/) [![Modal](https://img.shields.io/badge/Modal-22C55E?style=for-the-badge&logo=modal&logoColor=white)](https://modal.com) |
| **Infrastructure** | [![CUDA](https://img.shields.io/badge/CUDA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-zone) |
| **Development Tools** | [![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/) [![TensorBoard](https://img.shields.io/badge/TensorBoard-FF6D00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/tensorboard) [![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/) |
| **Documentation** | [![Markdown](https://img.shields.io/badge/Markdown-F37626?style=for-the-badge&logo=markdown&logoColor=white)](https://www.markdownguide.org/) [![TSV](https://img.shields.io/badge/TSV-1572B6?style=for-the-badge&logo=tabler&logoColor=white)](https://en.wikipedia.org/wiki/Tab-separated_values)|
---

## Project Structure

The repository is organized into the following directories:

- **Dataset Access**: Contains the Jupyter notebooks  accessing and downloading the non-standard speech dataset hosted by [Centre for Digital Language Inclusion](https://cdl-inclusion.com/) 🌐.
- **Evaluation**: Includes the jupyter notebooks for evaluating the performance of different models on the datasets. This is where you can find the results of my experiments and comparisons between various results for each whisper model.
- **Finetuning**: This directory holds the jupyter notebook used for fine-tuning the Whisper models. It includes the jupyter notebook for accessing  the data, setting up the training process, and running the fine-tuning jobs.
- **Inference**: Here, you will find the Jupyter notebook for running inference & results.

- 📒 Forked repository used for modal tooling:  [Centre for Digital Language Inclusion Modal Tooling Repository](https://github.com/cdl-inclusion/modal_tooling)

----
## Models

The fine-tuned models I've worked on will be stored on my hugging face that I've referenced above ☝🏾.

----

## Contact Information
[![Linktree](https://img.shields.io/badge/LexMainye-39E09B?style=flat&logo=linktree&logoColor=white)](https://linktr.ee/mainye)
