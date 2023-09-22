# Django-ChatApp

Django-ChatApp is a real-time chat application that allows users to communicate with each other instantly. It provides a seamless and interactive messaging experience for users to send and receive messages in real-time.

## Features

- **Real-Time Messaging:** ChatApp enables real-time communication, allowing users to exchange messages instantly.
- **User Authentication:** Secure user authentication and authorization to protect user data and privacy.
- **One-to-One Chat:** Users can engage in one-to-one private conversations.
- **Friends Recommendation:** Top 5 friend recommendations can be done based on interests and age.
- **Swagger-UI** This project features swagger-ui using drf-yasg

## Technologies Used

- **Backend:** Django , djangorestframework , channels
- **Database:** sqlite3
- **Authentication:** Token-based authentication

### Installation

1. Clone the repository:

```bash
git clone https://github.com/anutom20/django-chat-app.git
```

2. create a venv and activate it

```bash
python3 -m venv venv
```

3. install the required dependencies

```bash
pip install -r requirements.txt
```

4. make db migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

5.  start the ASGI dev server

```bash
python manage.py runserver
```

access application at http://localhost:800

### Documentation

swagger docs : http://localhost:8000/chatapp/docs

### Usage

1. open browser and go to http://localhost:8000/chatapp/api/register to get register template
2. Go to http://localhost:8000/chatapp/api/login to login template
3. Go to http://localhost:8000/chatapp/api/chat/{username}/ template to start real-time chat with a user , open another window to chat with the user in the first window
4. the api endpoints where templates are returned , don't work with swagger-ui
5. rest endpoints of logout , get-online-users , start chat can be tested through swagger-ui
6. for the friends top 5 recommendation list , go to http://localhost:8000/chatapp/api/suggested-friends/{id} , where id is the id of the user you want to recommend friends for

### Contact

Email : anuragkt20@gmail.com
linkedin : https://www.linkedin.com/in/anurag-tomar-2a26b51b3/

Happy Chatting!!
