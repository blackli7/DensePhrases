import json
import argparse
import torch
import os
import random
import numpy as np
import requests
import logging
import math
import copy
import string
import faiss

from time import time
from tqdm import tqdm

from densephrases.utils.open_utils import load_query_encoder, load_phrase_index, get_query2vec, load_qa_pairs

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s', datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def embed_query(question, args, query_encoder, tokenizer, batch_size=1):
    query2vec = get_query2vec(
        query_encoder=query_encoder, tokenizer=tokenizer, args=args, batch_size=batch_size
    )
    all_outs = []
    for q_idx in tqdm(range(0, len(question), batch_size)):
        print(question[q_idx:q_idx+batch_size])
        outs = query2vec(question[q_idx:q_idx+batch_size])
        all_outs += outs
    start = np.concatenate([out[0] for out in all_outs], 0)
    end = np.concatenate([out[1] for out in all_outs], 0)
    query_vec = np.concatenate([start, end], 1)
    #logger.info(f'Query reps: {query_vec.shape}')
    return query_vec

def evaluate(question, args, mips=None, query_encoder=None, tokenizer=None):
    # Load dataset and encode queries
    if query_encoder is None:
        print(f'Query encoder will be loaded from {args.query_encoder_path}')
        device = 'cuda' if args.cuda else 'cpu'
        query_encoder, tokenizer = load_query_encoder(device, args)
    query_vec = embed_query(question, args, query_encoder, tokenizer)

    # Load MIPS
    if mips is None:
        mips = load_phrase_index(args)

    # Search
    step = 1
    #logger.info(f'Aggergation strategy used: {args.agg_strat}')
    predictions = []
    evidences = []
    titles = []
    scores = []
    se_poss = []
    for q_idx in tqdm(range(0, len(question), step)):
        result = mips.search(
            query_vec[q_idx:q_idx+step],
            q_texts=question[q_idx:q_idx+step], nprobe=args.nprobe,
            top_k=args.top_k, max_answer_length=args.max_answer_length,
            aggregate=args.aggregate, agg_strat=args.agg_strat,
        )
        prediction = [[ret['answer'] for ret in out] if len(out) > 0 else [''] for out in result]
        evidence = [[ret['context'] for ret in out] if len(out) > 0 else [''] for out in result]
        title = [[ret['title'] for ret in out] if len(out) > 0 else [['']] for out in result]
        score = [[ret['score'] for ret in out] if len(out) > 0 else [-1e10] for out in result]
        se_pos = [[(ret['start_pos'], ret['end_pos']) for ret in out] if len(out) > 0 else [(0,0)] for out in result]
        predictions += prediction
        evidences += evidence
        titles += title
        scores += score
        se_poss += se_pos

    pred_out = {
                'question': question[0],
                'prediction': predictions[0], 'score': scores[0], 'title': titles[0],
                'evidence': evidences[0] if evidences is not None else '',
        }
    with open(args.question_test_out, 'w') as f:
            json.dump(pred_out, f)
    
    return prediction


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # QueryEncoder
    parser.add_argument('--model_type', default='bert', type=str)
    parser.add_argument("--pretrained_name_or_path", default='SpanBERT/spanbert-base-cased', type=str)
    parser.add_argument("--config_name", default="", type=str)
    parser.add_argument("--tokenizer_name", default="", type=str)
    parser.add_argument("--do_lower_case", default=False, action='store_true')
    parser.add_argument('--max_query_length', default=64, type=int)
    parser.add_argument("--cache_dir", default=None, type=str)
    parser.add_argument("--query_encoder_path", default='', type=str)
    parser.add_argument("--query_port", default='-1', type=str)

    # PhraseIndex
    parser.add_argument('--dump_dir', default='dump')
    parser.add_argument('--phrase_dir', default='phrase')
    parser.add_argument('--index_dir', default='256_flat_SQ4')
    parser.add_argument('--index_name', default='index.faiss')
    parser.add_argument('--idx2id_name', default='idx2id.hdf5')
    parser.add_argument('--index_port', default='-1', type=str)

    # These can be dynamically changed.
    parser.add_argument('--max_answer_length', default=10, type=int)
    parser.add_argument('--top_k', default=10, type=int)
    parser.add_argument('--nprobe', default=256, type=int)
    parser.add_argument('--aggregate', default=False, action='store_true')
    parser.add_argument('--agg_strat', default='opt1', type=str)
    parser.add_argument('--truecase', default=False, action='store_true')
    parser.add_argument("--truecase_path", default='truecase/english_with_questions.dist', type=str)

    # Run mode
    parser.add_argument('--run_mode', default='eval')
    parser.add_argument('--cuda', default=False, action='store_true')
    parser.add_argument('--draft', default=False, action='store_true')
    parser.add_argument('--debug', default=False, action='store_true')
    parser.add_argument('--save_pred', default=False, action='store_true')
    parser.add_argument('--seed', default=1992, type=int)

    #query encoder for step1
    parser.add_argument('--question_test_out', default='step1_question_test_out.json')

    args = parser.parse_args()

    question = input("just input what you want to ask (relevant to the sample articles) : \n")
    predictions = evaluate([question], args)
    print()
    print("############### Answer: ################")
    print(predictions[0][0])