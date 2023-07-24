# LLM Security Evaluation
This repo contains scripts for evaluating LLM security abilities. We gathered hundreds of questions cover different ascepts of security, such as vulnerablities, pentest, threat intelligence, etc.

All the questions can be viewed at [https://huggingface.co/datasets/c01dsnap/LLM-Sec-Evaluation](https://huggingface.co/datasets/c01dsnap/LLM-Sec-Evaluation).

## Suppoted LLM
* ChatGLM
* Baichuan
* Vicuna ([GGML format](https://huggingface.co/TheBloke/vicuna-13b-v1.3.0-GGML))
* LLaMA (HuggingFace format)

## Usage
Because of different LLM requires for different running environment, we highly recommended to manage your virtual envs via Miniconda.

1.Install dependencies
```bash
pip install -r requirements.txt

# If you want to use GPU, please install llama-cpp-python with the following command
LLAMA_CUBLAS=1 CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall --verbose
```
2.Clone this repo
```bash
git clone https://github.com/Coldwave96/LLM-Sec-Evaluation
cd LLM-Sec-Evaluation
```
3.Run bash scripts
```bash
# You might need to modify the script running interpreter in evaluate.py
bash evaluate.sh
```

## Changelog
- 2023.7.13 - Add support for ChatGLM & Baichuan
- 2023.7.17 - Add support for Vicuna
- 2023.7.24 - Add support for LLaMA
