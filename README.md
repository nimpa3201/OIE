# relation-analysis-engine

# Arguments
    1. --config_path [dir]    config.xml의 경로, default 사용권장
    2. --cleaning             특수문자 제거를 원하면 입력
    3. --spell check          맞춤법 검사를 원하면 입력
    4. --tokenizer [sp, morph, tokenizer]          사용할 토크나이징 방식 선택 
    5. --process_dict         사전 처리를 원하면 입력
    6. --save_output          결과값 저장을 원하지 않으면 입력
    7. --predict_ner          ner값 예측&예측값 저장을 원하면 입력
    8. --data_dir [dir]       label.txt의 위치, default 사용권장
    9. --output_file [dir]    ner예측값 결과파일의 위치, default 사용권장
    10. --model_dir [dir]     model의 경로, default 사용권장
    11. --max_seq_len [int]   tokens의 최대 길이, 해당 값을 넘는 문장은 해당 길이까지만 예측
    12. --batch_size_ner [int] batch_size설정
    13. --no_cuda_ner         cuda 사용유무, cuda 사용을 원하지 않으면 입력


# Use

    python main.py --tokenizer sp --predict_ner

--max_seq_len 변경과 --cleaning 사용은 선택사항
