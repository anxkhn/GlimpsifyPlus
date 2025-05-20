## Examples

### Video is already downloaded in local directory and you want to extract key moments

`python main.py --input=local --dir=x`

> NOTE: The video is in the directory `data/x`

### Video is on youtube and you want to extract key moments

`python main.py --input=youtube --url="https://www.youtube.com/watch?v=PmvLB5dIEp8&list=PL8dPuuaLjXtONguuhLdVmq0HTKS0jksS4&index=3" --cleanup --k=15 --ocr=tesseract`

> NOTE: The `url` is in double quotes as it contains special characters

### Video is a playlist and you want to extract key moments

`python main.py --input=playlist --url="https://www.youtube.com/playlist?list=PL8dPuuaLjXtONguuhLdVmq0HTKS0jksS4" --start_from=3 --cleanup`

> NOTE: The `url` is in double quotes as it contains special characters \
>
> The `start_from` parameter is optional and is used to skip the first n videos in the playlist

### Video is on YouTube and you want to extract key moments using timestamps

`python main.py --input=youtube --url="https://www.youtube.com/watch?v=_8xHh1tk7jY&t=165s" --extraction=timestamps`

`python main.py --input=youtube --url="https://www.youtube.com/watch?v=_8xHh1tk7jY&t=165s" --extraction=timestamps`
`python main.py --input=youtube --url="https://www.youtube.com/watch?v=_8xHh1tk7jY&t=165s" --extraction=timestamps --timestamps=[1, 2, 3]`
`python main.py --input=youtube --url="https://www.youtube.com/watch?v=_8xHh1tk7jY&t=165s"`
`python main.py --input=local --dir=cpdnaj --extraction=prominent_peaks`


