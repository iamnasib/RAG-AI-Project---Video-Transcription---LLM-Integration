import os
import json
import math

number_of_chunk_to_merge=5

for file in os.listdir('jsons'):
    with open(f'jsons/{file}', 'r', encoding='utf-8') as f:
        data = json.load(f)
        new_chunks=[]
        count_of_chunks=len(data['chunks'])
        chunk_groups=math.ceil(count_of_chunks/number_of_chunk_to_merge)

        for i in range(chunk_groups):
            strt_idx=i*number_of_chunk_to_merge
            end_idx=min((i+1)*number_of_chunk_to_merge,count_of_chunks)

            chunk_grouped=data['chunks'][strt_idx:end_idx]
            new_chunks.append({
                "video_number":data['chunks'][0]["video_number"],
                "video_title":data['chunks'][0]["video_title"],
                "start":chunk_grouped[0]["start"],
                "end":chunk_grouped[-1]["end"],
                "text":" ".join([c["text"] for c in chunk_grouped])
            })
        os.makedirs("newJsons", exist_ok=True)
        with open(f"newJsons/{file}","w",encoding="utf-8") as new_json:
            json.dump({'chunks':new_chunks,"text":data['text']}, new_json, indent=4)
