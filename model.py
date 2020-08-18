import os
import sys

import torch
import torch.nn as nn

from transformers import AutoTokenizer
from transformers import BertForSequenceClassification

import re

from konlpy.tag import Mecab


top_k = 5
gpu_id = -1

'''
메캅설치 참조 : https://konlpy-ko.readthedocs.io/ko/v0.4.3/install/
'''

def read_text(text):
    '''
    Read text from standard input for inference.
    '''
    lines = []
    
    for line in [text]:
        if line.strip() != '':
            temp = re.sub(r'[○▶\-\+=,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》\r\n\t＊→★▲▼■□ㅇ_;]', ' ', line.strip())
            pattern = re.compile(r'\s\s+')
            temp = re.sub(pattern, ' ', temp)
            lines += [temp]
    print(lines)
    return lines # list

def predict(text):
    top_k = 5
    saved_data = torch.load(
        'kcbert_novalid_9.pth', map_location='cpu')
        # map_location='cpu' if config.gpu_id < 0 else 'cuda:%d' % config.gpu_id

    train_config = saved_data['config']
    bert_best = saved_data['bert']
    index_to_label = saved_data['classes']

    lines = read_text(text)
    mecab = Mecab()
    mc_lines = mecab.morphs(lines[0])
    texts = ' '.join(mc_lines)
    print(texts)
    

    with torch.no_grad():
        # Declare model and load pre-trained weights.
        tokenizer = AutoTokenizer.from_pretrained(train_config.pretrained_model_name)
        model = BertForSequenceClassification.from_pretrained(
            train_config.pretrained_model_name,
            num_labels=len(index_to_label)
        )
        model.load_state_dict(bert_best)

        if gpu_id >= 0:
            model.cuda(gpu_id)
        device = next(model.parameters()).device

        # Don't forget turn-on evaluation mode.
        model.eval()

        mini_batch = tokenizer(
            [texts],
            padding=True,
            truncation=True,
            return_tensors="pt",
        )

        x = mini_batch['input_ids']
        x = x.to(device)
        mask = mini_batch['attention_mask']
        mask = mask.to(device)

        # Take feed-forward
        y_hat = model(x, attention_mask=mask)[0]
        # print(y_hat)
        probs = nn.Softmax(dim=1)
        softmax_output = probs(y_hat)
        print(softmax_output)

        probs, indice = softmax_output.cpu().topk(top_k)
        # |indice| = (len(lines), top_k)
        print(indice)
        print(probs)

        results = [index_to_label[int(indice[0][j])] for j in range(top_k)]
        probs = [round(probs[0][j].item(),4) for j in range(top_k)]
        res = list(zip(results,probs))

    return res


    ###########################
    # .모델 변경 방식 미반영
    # .서버, JSON 방식 미반영
    # return {
    #     'code':'SUCESS',
    #     'result': result
    # }
    ###########################




