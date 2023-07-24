python evaluate.py \
    --model_name ChatGLM \
    --model_path /home/max/Documents/ChatGLM2-6B/chatglm2-6b

python evaluate.py \
    --model_name Baichuan \
    --model_path /home/max/Documents/Baichuan-13B/Baichuan-13B-Chat \
    --load_8bit True

python evaluate.py \
    --model_name Vicuna \
    --model_path /home/max/Documents/vicuna-13B-GGML/vicuna-13b-v1.3.0.ggmlv3.q8_0.bin

python evaluate.py \
    --model_name LLaMA \
    --model_path /home/max/Documents/llama-2/llama-2-7b-chat-hf
