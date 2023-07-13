# LLM Security Evalustion
This repo contains scripts for evaluating LLM security abilities. We gathered hundreds of questions cover different ascepts of security, such as vulnerablities, pentest, threat intelligence, etc.

All the questions can be viewed at [https://huggingface.co/datasets/c01dsnap/LLM-Sec-Evaluation](https://huggingface.co/datasets/c01dsnap/LLM-Sec-Evaluation).

## Suppoted LLM
* ChatGLM
* Baichuan

## Usage
Because of different LLM requires for different running environment, we highly recommended to manage your virtual envs via Miniconda.

1.Install dependencies
```bash
pip install -r requirements.txt
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
