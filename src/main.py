# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys, time, os, argparse
from scd_parser import scd_validation,parser_main
#from pre_processor import tokenizer, preprocess_dict, spell_check
from kobert_ner import predict
import pickle_def as pickle



def main(args):
    start = time.time()

    tree = ET.parse(args.config_path)
    root = tree.getroot()


    scd_validation.validation_main(root)


    doc_list = parser_main.parser_main(root,args)
    print("여기까지가 파서  "+str(time.time()-start))

    if args.spell_check:
        doc_list = spell_check.spell_main(root, doc_list)
        print("여기까지가 스펠체크  "+str(time.time()-start))


    doc_list, orignal = tokenizer.token_main(root, args, doc_list)
    print("여기까지가 토크나이저  "+str(time.time()-start))


    if args.process_dict:
        doc_list = preprocess_dict.dict_main(root, args, preprocess_dict.dict_main(root, args, doc_list, 'stopword'), 'synonym')
        print("여기까지가 사전처리  "+str(time.time()-start))
  

    if args.predict_ner:
        ner_texts = predict.predict(args, doc_list, orignal)

    if args.save_output:
        with open(os.path.join(".\..","output.txt"),"w",encoding='UTF-8') as r:
            for i in doc_list:
                r.write(str(i))
                r.write("\n\n")
    return doc_list







if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--config_path", type=str, default=".\..\config\config.xml",
                        help="패키지의 config.xml의 상대경로")

    parser.add_argument("--cleaning", action="store_true", help="특수 문자 제거를 원한다면 입력")
    parser.add_argument("--spell_check", action="store_true", help="맞춤법 검사를 원한다면 입력")
    parser.add_argument("--tokenizer", type=str, default='sp', help="사용할 토크나이저 선택 (sp, morph, tokenizer)")
    parser.add_argument("--process_dict", action="store_true", help="사전 처리를 원한다면 입력")
    parser.add_argument("--save_output", action="store_false", help="OUTPUT저장을 원하지 않으면 입력")

    parser.add_argument("--predict_ner", action="store_true", help="ner 값 예측을 원한다면 입력")
    parser.add_argument("--data_dir", default=".\kobert_ner\data", type=str, help="label.txt의 경로")
    parser.add_argument("--output_file", default=".\..\pred_out.txt", type=str, help="Output file for prediction")
    parser.add_argument("--model_dir", default=".\kobert_ner\model", type=str, help="Path to save, load model")

    parser.add_argument("--max_seq_len", default=100, type=int, help="max_len of sentence")
    parser.add_argument("--batch_size_ner", default=32, type=int, help="Batch size for prediction")
    parser.add_argument("--no_cuda_ner", action="store_true", help="Avoid using CUDA when available")


    args = parser.parse_args()
    

    main(args)


ner_output = main(args)
print(ner_output)




