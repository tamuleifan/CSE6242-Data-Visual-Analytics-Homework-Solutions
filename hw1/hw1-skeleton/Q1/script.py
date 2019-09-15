import http.client
import json
import time
import sys
import collections


###########
#part b
###########
script_start = time.time()
print('=== part b: movie name and movie id ===')
#get api_key from command line input
api_key = sys.argv[1].strip()

#container = collections.OrderedDict()
container = list()

#18 requests will get 18 pages with 360 movies, then delete the last 10 to get 350
n_requests = 18

#connet the server
conn = http.client.HTTPSConnection("api.themoviedb.org", timeout = 20)
payload = "{}"

print("retrieving data from TMDB...")

#submit the request page by page, 18 totally
for i in range(n_requests):   
#genres = 18 for drama
    url = "/3/discover/movie?with_genres=18&primary_release_date.gte=2004-01-01&page="+str(i+1)+"&sort_by=popularity.desc&api_key="+str(api_key)
    conn.request("GET", url ,payload)

    res = conn.getresponse()
    data = res.read()
    #decode into json format
    json_data = json.loads(data)
    #extract movie id and name and store them in a list
    for i in range(len(json_data['results'])):
        container.append([str(json_data['results'][i]['id']), json_data['results'][i]['title']])
#slice the list to get 350 items as asked
container = container[:350]

print("data downloaded")

#save the list item into a csv file
with open('movie_ID_name.csv', 'w+') as f:
    for item in container:
        f.write("{},{}\n".format(item[0], item[1]))
        
print("movie_ID_name.csv created")
print('{}s used'.format(round((time.time()-script_start),2)))
print("================================")


###########
#part c 
############

script_start = time.time()
print('=== part c: similar movie id ===')
container_2 = list()

conn = http.client.HTTPSConnection("api.themoviedb.org",timeout = 20)
payload = "{}"

print("retrieving data from TMDB...")

for item in container:
    request_start = time.time()
    source_id = item[0]
    ######
    url_2 = "/3/movie/{}/similar?page=1&api_key={}".format(source_id,str(api_key))
    conn.request("GET", url_2, payload)

    res_2 = conn.getresponse()
    data_2 = res_2.read()
    json_data_2 = json.loads(data_2)
    m = min(5,len(json_data_2['results']))
    for i in range(m):
        container_2.append([source_id, json_data_2['results'][i]['id']])
    time_elapsed = time.time()-request_start
    #every 10 secs 40 requests are allowed at most
    if time_elapsed <0.25:
        time.sleep(0.25 - time_elapsed)

#extract the orginal movie id
orginal_id_container = [item[0] for item in container]
#step2:deduplication
for item in container_2:
    #if the similar movie id were also in the list of the original ones, then duplication spotted
    if item[1] in orginal_id_container and [item[0],item[1]] in container_2 and [item[1],item[0]] in container_2:
        #remove duplicate pairs starting with large id
        id_min = min(item[0], item[1])
        id_max = max(item[0], item[1])
        #if [id_max,id_min] in container_2:
        container_2.remove([id_max,id_min])
print("data downloaded")

#save the list item into a csv file
with open('movie_ID_sim_movie_ID.csv', 'w+') as f:
    for item in container_2:
        f.write("{},{}\n".format(item[0], item[1]))
print("movie_ID_sim_movie_ID.csv created")
print('{}s used'.format(round((time.time()-script_start),2)))