#! /home/max/miniconda3/envs/llm-sec-eval/bin/python

import os
import sys
import time
import torch
import argparse
import pandas as pd

from transformers import (
    AutoTokenizer,
    AutoModel,
    AutoModelForCausalLM
)
from transformers.generation.utils import GenerationConfig
from llama_cpp import Llama
from vllm import LLM, SamplingParams

supported_models = ["ChatGLM", "Baichuan", "Vicuna", "LLaMA"]

parser = argparse.ArgumentParser(description="Scripts for testing LLM sec abilities.")
parser.add_argument("--model_name", type=str, required=True, 
                    help=f"Specify the model you want to evaluate (Choose from: {str(supported_models)})")
parser.add_argument("--model_path", type=str, required=True, help="Sepcify the directory of model")
parser.add_argument("--question_file", type=str, default="question-default.xlsx", 
                    help="Specify the csv or xlsx file which contains questions")
parser.add_argument("--load_8bit", type=bool, default=False, help="Load 8 bit quantized model, default value False")
args = parser.parse_args()

# Load Model
print(f"[*] Loading model {args.model_name}...")
match args.model_name:
    case "ChatGLM":
        tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
        model = AutoModel.from_pretrained(args.model_path, trust_remote_code=True)
        if args.load_8bit:
            model = model.quantize(8)
        model = model.cuda()
        model.eval()
    case "Baichuan":
        tokenizer = AutoTokenizer.from_pretrained(args.model_path, use_fast=False, trust_remote_code=True)
        if args.load_8bit:
            model = AutoModelForCausalLM.from_pretrained(args.model_path, torch_dtype=torch.float16, trust_remote_code=True)
            model = model.quantize(8).cuda()
        else:
            model = AutoModelForCausalLM.from_pretrained(args.model_path, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True)
        model.generation_config = GenerationConfig.from_pretrained(args.model_path)
    case "Vicuna":
        model = Llama(model_path=args.model_path, n_ctx=2048, n_gpu_layers=256)
    case "LLaMA":
        model = LLM(args.model_path, tensor_parallel_size=1)
    case _:
        print(f"{args.model_name} is not supported yet! Please choose from {str(supported_models)}")
        sys.exit(0)

print("[*] Successfully load the model.")

# Load Evaluation Data
print(f"[*] Loading question file {args.question_file}...")
if os.path.exists(args.question_file):
    if str(args.question_file).endswith(".csv"):
        question_df = pd.read_csv(args.question_file)
    elif str(args.question_file).endswith(".xlsx"):
        question_df = pd.read_excel(args.question_file)
    print("[*] Successfully load the question file.")
else:
    print(f"Error! File {args.question_file} does not exist.")
    sys.exit(0)

print("[*] Start evaluating...")
output_df = pd.DataFrame()
for i_question, row_question in question_df.iterrows():
    prompt = f"""{row_question["question"]}"""
    time_start = time.time()
    match args.model_name:
        case "ChatGLM":
            response, history = model.chat(tokenizer, prompt, history=[])
        case "Baichuan":
            messages = []
            messages.append({"role": "user", "content": prompt})
            response = model.chat(tokenizer, messages)
        case "Vicuna":
            messages = "Q: " + prompt + " A: "
            output = model(messages, max_tokens=1024, stop=["Q:"], echo=True)
            response = output["choices"][0]["text"].split("A: ")[1].strip()
        case "LLaMA":
            sampling_params = SamplingParams(top_p=0.95, temperature=0.8, top_k=40, max_tokens=2048)
            outputs = model.generate(prompt, sampling_params=sampling_params)
            response = outputs[0].outputs[0].text.strip()
            if response.startswith("？"):
                response = response[1:].split("</s>")[0].strip()
    time_end = time.time()
    temp = pd.DataFrame(
        {
            'question': row_question["question"],
            f'{args.model_name}': response,
            'time_spend': time_end - time_start
        },
        index = [output_df.size]
    )
    output_df = pd.concat([output_df, temp], ignore_index=True)

    if i_question % 10 == 0:
        print(f"Total amount: {question_df.shape[0]}, finished No.{i_question} already...")

output_file = "outputs/output-" + args.model_name + ".xlsx"
output_df.to_excel(output_file)
print(f"[*] Successfully finished evalustion process, please check {output_file} for detailed results.")
