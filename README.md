## Sentinel: A Highly Scalable and Powerful Chat Application facilitating messaging between individuals for seamless communication.

### Product Key Features:

1. Users are able to create and login to their accounts in order to access the application.
2. One-to-one messaging: users are able to send and receive text messages, images, files.
3. Users are able to see the status of messages they have send in form of read receipts.
4. Users are able to load older messages and chat history.
5. Users are able to see which other user is active or inactive on a real-time basis.
6. Users are able to search for a message throughout the chat history.
7. Chat application is able to send notifications to the user when they receive a message.

### Some other features:

1. Scalability. Our application is going to have millions of active users and thus the system are highly scalable and available to handle such amount of traffic.
2. Consistency in terms of data. Users are able to see very older messages as well.
3. Real time response to events such as changed user state from active to inactive.
4. Fast search through the chat history.

### Summary

* We could go with the micro-service architecture to have decoupling and effective scalling and management of our services.
* Users Service:
    * The Users Service handles user registration and login functionalities for the web application. Upon successful login, user credentials including hashed passwords and email addresses are stored in a Postgres database according to the defined user schema.
    * Additionally, the Users Service facilitates user searches by username, returning the corresponding username and user ID upon finding an exact match.
* Message Service:
    * Leveraging web sockets for its bidirectional communication capabilities.
    * Users can search for others by username and initiate conversations via a button, establishing a websocket connection between them. Each user is uniquely identified by their user ID, and a private room with a unique ID is created for the conversation.
    * Messages sent by users are stored in the message table along with sender ID, message ID, chat ID, and other relevant attributes.
    * Message retrieval involves querying the message table based on the chat ID.
    * To obtain the chat IDs associated with a user, the user_chat association table is queried to retrieve the chat ID linked to the respective user.
* Notification Service:
    * Adopting the Producer/Consumer pattern offers a solution for decoupling processes involved in producing and consuming notifications, especially when these processes operate at different rates. Utilizing Kafka, a scalable message broker, becomes advantageous, particularly when dealing with large volumes of data and high loads.
    * Notifications, which are events triggered by various actions within the web application such as user registration or message sending, will be generated and published to designated topics.
    * A consumer component will be implemented to subscribe to these events, processing them through Firebase Cloud Messaging (FCM) to generate notifications within the web application.
* Search Service:
    * Leveraging ElasticSearch for message searching provides a robust solution. Initially, data from Cassandra will be indexed into ElasticSearch, allowing efficient querying of messages.
    * ElasticSearch (ES) is chosen for its speed and scalability. It offers the capability to subdivide indexes into multiple shards, each of which functions as an independent "index" and can be hosted on any node within a cluster.
    * Distributing documents across multiple shards and nodes ensures redundancy, safeguarding against hardware failures and enhancing query capacity with the addition of nodes to the cluster.
    * Asynchronous search functionality across these shards enables rapid retrieval of results, with the ability to segment messages based on timestamp or other relevant fields, further enhancing search performance.
* Users Presence Service:
    * We could implement a heartbeat mechanism, employing a worker process to regularly ping clients and monitor user activity. By continuously checking for interactions, this mechanism ensures that we stay informed about user presence and can take appropriate actions if users become inactive.
    * For swift storage and retrieval of user activity data, we could utilize a Redis cluster for caching. This would allow us to promptly store and access timestamps of user activity, facilitating efficient management of user presence.
    * After storing user activity timestamps, we could compare them against a predefined threshold to identify periods of prolonged inactivity. If a user remains inactive beyond this threshold, we could automatically mark them as inactive, ensuring that our system accurately reflects user presence in real-time.

### Components

#### REST API

We’ll create our services as Flask applications which handles actions like user login and register, table creation, data retrievals. 


#### Websocket 

WebSockets are a bi-directional, full duplex communications protocol initiated over HTTP. connections are typically long-lived. Messages can be sent in either direction at any time and are not transactional in nature. The connection will normally stay open and idle until either the client or the server is ready to send a message.


#### Apache Kafka

Kafka is a distributed event streaming platform that lets you read, write, store, and process events (also called records or messages in the documentation) across many machines.
The purpose of Kafka in the solution is to decouple producer (database) and consumer (which can be multiple) and to be able to scale to millions of events or notifications. It provides a free flow of data into topics which can be extracted, transformed and loaded into multiple sinks. 
Different topics can be created for different use cases to store events such new user registration or new messages, and any number of sinks can subscribe to the topics for ingesting data.


#### Cassandra

For storing messages, we'll consider using a NoSQL database, such as Cassandra.  Since it is a distributed database, Cassandra can (and usually does) have multiple nodes. A node represents a single instance of Cassandra. These nodes communicate with one another through a protocol called gossip, which is a process of computer peer-to-peer communication. Cassandra also has a masterless architecture – any node in the database can provide the exact same functionality as any other node – contributing to Cassandra’s robustness and resilience. Multiple nodes can be organized logically into a cluster, or "ring".

Through multiple nodes we can easily scale out or horizontally scale the database.

In Cassandra, the data itself is automatically distributed using partitions. Each node owns a particular set of tokens, and Cassandra distributes data based on the ranges of these tokens across the cluster. The partition key is responsible for distributing data among nodes and is important for determining data locality. When data is inserted into the cluster, the first step is to apply a hash function to the partition key. The output is used to determine what node (based on the token range) will get the data.

CREATE TABLE IF NOT EXISTS messages (
        message_id UUID,
        chat_id UUID,
        sender_id UUID,
        type TEXT,
        timestamp TIMESTAMP,
        content TEXT,
        seen_at TIMESTAMP,
        PRIMARY KEY ((chat_id), timestamp, message_id)
    )
    WITH CLUSTERING ORDER BY(timestamp DESC);

* 'chat_id' will be the partition key and timestamp, message_id the clustering key. 
* We specified timestamp DESC inside of CLUSTERING ORDER BY. It's important to note that 'message_id' will serve for uniqueness purposes in this design.

#### NGINX 

Nginx sits in front of your application servers and acts as a reverse proxy. Client requests are first directed to Nginx, which then forwards those requests to one of the backend servers. We have taken 2 servers as of now to distribute load to. 

upstream message_service {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    # Add more servers if needed
}

By default, Nginx uses the Round Robin load balancing algorithm to distribute incoming traffic across the defined upstream servers. With Round Robin, Nginx forwards each new request to the next server in the upstream block in a sequential manner. This means that each server receives an equal share of incoming requests over time, without consideration of the server's current load or performance.


#### Postgres

We have utilised the SQL database postgres to store the user details and credentials.


#### Elastic Search

We can leverage the elastic Search a powerful distributed, open-source search and analytics engine built on Apache Lucene. Data from Cassandra will be indexed into Elasticsearch. Elasticsearch (ES) is chosen for its speed and scalability. It offers the capability to subdivide indexes into multiple shards, each of which functions as an independent "index" and can be hosted on any node within a cluster.

* Asynchronous search functionality across multiple shards can be used for rapid retrieval of results, with the ability to segment messages based on timestamp or other relevant fields, further enhancing search performance.



### High Level Design:

1. We could go with the micro-service architecture where we’ll have: 
    1. Users Service
    2. Message Service
    3. Notification Service
    4. Search Service
    5. Users Presence service
    6. Media Service


##### Users Service:

1. Users is registered and the credentials are stored in the database.
2. Registered user are able to login to use the chat application.
3. This service will use JWT for secure authentication and authorisation.
4. Users database will be a postgres that will store all the user details and credentials.

##### Message Service:

1. It’ll be a python flask application that’ll handle the one-to-one messaging feature.
2. To handle high loads, we'll deploy multiple instances of the message service and utilize load balancers to distribute incoming traffic evenly across these instances, ensuring optimal performance and scalability.
3. For storing messages, we'll consider using a NoSQL database, such as Cassandra. 
4. Since it is a distributed database, Cassandra can (and usually does) have multiple nodes. See “Cassandra Component“ section for more details.
5. To enable real-time messaging, we'll integrate WebSocket connections, allowing for bi-directional communication between clients and servers. 
6. Retrieving chat history will involve querying the database for messages associated with the relevant users. We'll implement pagination to display messages in batches, along with a "load more messages" button feature to fetch additional messages as needed.
7. The messages should also be stored hashed and not be visible it are encrypted.
8. To enhance performance, we'll implement caching to store the most recent chats locally. This cached data will be quickly accessible upon user login, providing a seamless and responsive user experience.

#### Users Presence Service:

1. This service is responsible for showing user the active status of other users whether they are active or not.
2. Create a database schema to store user information, including their status.
3. Include fields like user_id, user_status, etc.
4. APIs will be implemented to update user status, such as when a user logs in or performs an action, and to retrieve the status of other users
5. The user's last active timestamp will be updated upon login and stored in Redis cache for fast retrieval, ensuring timely and accurate status updates.
6. To periodically update user status, we'll create a worker application or implement a heartbeat mechanism. This mechanism will regularly check user activity and update their status accordingly, providing real-time visibility into user availability.

#### Notification Service:

1. We have adopted the Producer/Consumer pattern which offers a solution for decoupling processes involved in producing and consuming notifications, especially when these processes operate at different rates. 
2. We have utilised Kafka, a scalable message broker.
3. Notifications, which are events triggered by various actions within the web application upon user registration and upon message sending.
4. These events generated and published to designated topics such as “received_message”.
5. A consumer component a long pooling service worker is subscribed to these events.
6. Websocket connection is created to push those notification to the client and create a alert message box.

#### Search Service:

1. We'll rely on ElasticSearch, a powerful tool for searching vast amounts of text rapidly. It'll create a dedicated space to index all the words and phrases from our messages.
2. We can create an index in ElasticSearch for message content.
3. Implement a search API on the backend that queries on ElasticSearch index.
4. The API should take search queries and return relevant messages.

#### Media Service:

1. For storing files and pictures, we'll use Amazon S3. It's like a giant closet in the cloud where we can keep things. When we put stuff in this closet, we get special web addresses (URLs) that we can use to find them later.
2. To make sure things load quickly, especially if lots of people are looking at them, we'll use something called CDNs, or Content Delivery Networks. These are like super-fast delivery trucks that carry our files and documents to people's computers really quickly, no matter where they are.



### Database:

##### Users:

* We’ll use postgres to store the user details using the above schema.
* This will provide us faster user details retrievals and insertion





#### Message:




#### Users Chat:


* We’ll user Cassandra to store the messages and the user_chat association table.
* Cassandra provides fast write operations we can replicate the nodes to maintain data availability.

### API Contracts:

Users Service:
```
POST: /register

req:
{
    username: String,
    password: String,
    email: String
}

response:
{
    access_token: String
    username: String,
    user_id: UUIDv4
}

POST: /login
req:
{
    username: String,
    password: String,
}
response:
{
    access_token: String
    username: String,
    user_id: UUIDv4
}

GET: /users/show

response:
{
    "users" = [
    {
        "username": String,
        "user_id": UUIDv4
    }, 
    {
        "username": String,
        "user_id": UUIDv4
    },..]
}

GET: /users/show?username={username}

response:
{
   "username": String,
   "user_id": UUIDv4
}

This api is returning the user with the given username 
by querying the postgres Users table with the matching records.
```
Websocket endpoints:
```
@socketio.on('connect', namespace='/chat')

- to connect the user to the messaging service

@socketio.on('disconnect', namespace='/chat')

- to disconnect user from the messaging service

@socketio.on('start_private_chat', namespace='/chat')

- checks if there exists a history of chat btw user1 and user2
- if exists then retrieve the chat_id
- if not then generate a new chat_id and insert it into the user_chat table along with
   user_id and timestamp
- creates a room for 2 users with room_id = chat_id
- users can connect to this room and exchange messages

@socketio.on('send_message', namespace='/chat')

- push the message into the database with the message_id chat_id, sender_id, etc (see the model schema for details)
- emit a receive_message event so that users can receive messages 
    whoever are listening to this event in the same room

@socketio.on('receive_message', namespace='/chat')

- sends an acknowledment to the users
```

Message Service:
```
GET: /users/chat?user_id={user_id}

- returns the chat_ids of all the chats user is part of 

GET: /users/chat/{chat_id}

- returns the messages of a chat with particular chat_id 
- sort the messages based on timestamp from newest to oldest
```
Users Presence Service:
```
GET: /users/user_activity?username={username}
res:
{
    "username": String,
    "active": Boolean
}

- this api returns the user status in form of "active" boolean, 
  true means user is currently active and vice-versa

GET: /users/update-last-active?user_id={user_id}

- this api update the last active timestamp of user with given user_id
- 
GET: /users/last_active?user_id={user_id}

res:
{
    "user_id": UUIDv4,
    "last_active_timestamp": timestamp
}

- this api gets the last active timestamp of a particular user based on the user_id
```
Notification Service:
```
@socketio.on("connect")
- connects the notification consumer client with the notification service 
```


### Pagination in cassandra:

We wanted to achieve pagination that is not showing all the messages to the user at once but splitting it into the pages. So, we wanted to fetch from our cassandra server only few messages of some size “chunks”, to speed up the process of fetching messages and loading chat history. Idea was to further store them in cache so, that they can get loaded pretty quickly when user visits the chat history.

Let's first understand how smartly SELECT * query is implemented in Cassandra. Suppose, you have a table with ~1B rows and you run -

```SELECT * FROM my_cassandra_table;```

Loading all the 1B rows into the memory is very tedious. Cassandra does it in a very smart way with fetching data in pages. so you don't have to worry about the memory. It just fetches a chunk from the database (~ 5000 rows) and returns a cursor for results on which you can iterate, to see the rows. 

Once our iteration reaches close to 5000, it again fetches the next chunk of 5000 rows internally and adds it to the result cursor. It does it so brilliantly that we don’t even feel this magic happening behind the scene.

When I deep-dived into Cassandra configurations I found that whenever Cassandra returns a result cursor, it brings a page state with it. Page state is nothing but a page number to help Cassandra remember which chunk to fetch next.


```
from cassandra.query import SimpleStatement
query = "SELECT * FROM my_cassandra_table;"
```

statement = SimpleStatement(query, fetch_size=100)
results = session.execute(statement)

# save page state
page_state = results.paging_state

for data in results:
    process_data_here(data)

* Based on our use case, we set the fetch size (it is the size of the chunk, manually given by us to Cassandra). And when we got the result cursor, we saved the page state in a variable.
* We put a check on the counter. If it exceeds the manual chunk size, it breaks and again fetches a fresh new chunk with the page state already saved.
* We saved the page_state in the redis, whenever the user press the load more button we get the latest page_state from the redis and use it to move forward the page_state cursor.




### Setting up NGINX as reverse proxy

```Install gunicorn: 

pip install gunicorn

Run  2 instances of message-service at port 5000 and 5001:

gunicorn -w 4 -b 127.0.0.1:5000 app.py:app
gunicorn -w 4 -b 127.0.0.1:5001 app.py:app

Configure NGINX:

pid       /usr/local/var/run/nginx.pid;

log_format upstreamlog '$server_name to: $upstream_addr [$request] ' 
'upstream_response_time $upstream_response_time '
'msec $msec request_time $request_time';

upstream message_service {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    # Add more servers if needed
}
server {
    listen 80;
    server_name localhost;
    access_log  /usr/local/var/log/nginx/access.log  upstreamlog;
    location / {
        proxy_pass http://message_service;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
    }
    # Additional configurations if needed
}

Test the nginx:
nginx -t     

Start nginx:
nginx

load the access logs:
sudo tail -f /usr/local/var/log/nginx/access.log

Change the config:
nano /usr/local/etc/nginx/nginx.conf

see the running brew services:
brew services    

reload nginx after changes in configs:
sudo nginx -s reload 

see all the nginx processes
ps aux | grep nginx

start nginx according to the configs:
sudo nginx -c /usr/local/etc/nginx/nginx.conf

start and stop config service
sudo brew services start nginx
sudo brew services stop nginx

get the ouput of nginx proxy by going to localhost (default port 80)
curl -g http://localhost/

When pid is not found

sudo brew services stop nginx

make dir if not found:
sudo mkdir -p /usr/local/var/run/

remove the pid file if not working permission denied by existing file:
sudo rm /usr/local/var/run/nginx.pid

create nignx at desired place by runnig cmmd -
sudo touch /usr/local/var/run/nginx.pid

check if pid is created succesfully -
sudo ls /usr/local/var/run/nginx.pid
output: /usr/local/var/run/nginx.pid

give access to the pid file:
sudo chmod 777 /usr/local/var/run/nginx.pid

start the nginx service:
sudo brew services start nginx

run nginx:
nginx

sudo nginx -c /usr/local/etc/nginx/nginx.conf

reload nginx:
sudo nginx -s reload
```




### Reference:

1. https://medium.com/@anirudhkanabar/clustering-order-in-cassandra-how-to-achieve-ordering-of-data-in-cassandra-f52e8a73d5d5
2. https://www.pankajtanwar.in/blog/pagination-with-cassandra-lets-deal-with-paging-large-queries-in-python?source=post_page-----97a60abe781c--------------------------------
3. https://medium.com/rahasak/index-cassandra-data-on-elasticsearch-with-akka-streams-6e9298a75190
4. https://thelastpickle.com/blog/2018/04/03/cassandra-backup-and-restore-aws-ebs.html
5. https://medium.com/rahasak/elassandra-936ab46a6516
6. https://medium.com/@cilesizemre/elasticsearch-cassandra-elassandra-9c5fb3d6fc86
7. https://kafka.apache.org/documentation/#producerapi
8. https://www.codurance.com/publications/2016/04/17/sorted-pagination-in-cassandra
9. https://medium.com/@VenuThomas/what-is-nginx-and-how-to-set-it-up-on-mac-107a2482a33a

### Indiviual Code Repos:

1. https://github.com/pixelcaliber/chat-app-message-service
2. https://github.com/pixelcaliber/notification-service
3. https://github.com/pixelcaliber/user-presence-service
4. https://github.com/pixelcaliber/chat-application-user-service

