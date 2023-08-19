to run just the script: (assigment 1)

python get_songs.py <keyword>


to build and run dockerfile:

docker build -t app:1.0 .
docker run -d -p 5000:5000 app:1.0 


then make an http request like that:

http://localhost:5000/get_songs?keyword=<keyword>

