import os
import whisper
import json

model=whisper.load_model('large-v2')

audios=os.listdir('audios')

for audio in audios:
    video_number, remainder=audio.split('_',1)
    video_title=remainder.split('.')[0]
    print(video_title,video_number)

    result=model.transcribe(audio="audios/"+audio, 
                     language="hi", task="translate", word_timestamps=False)



    chunks=[]
    for segment in result['segments']:
        chunks.append({'video_number':video_number, 'video_title':video_title,'start':segment['start'], 'end':segment['end'],'text':segment['text'].strip()})
        
    chunk_with_metadata={"chunks":chunks,"text":result["text"]}

    with open(f"jsons/{audio}.json", "w") as f:
        json.dump(chunk_with_metadata,f)
