# travel_mate
Python + Fast API + Llm demo project

If you are starting a fresh project
---------
$ mkdir <your-project-directory>
$ cd <your-project-directory>

#fix the python version for eg., 3.12
$ uv init --python 3.12
$ rm main.py

Install dependencies.
for eg.,
$ uv add openai-agents

If you are checking out uv project from github
-------------------
You just need to synch the dependencies
$ uv sync

$ docker-compose up -d

Get into postgre container shell and execute create script
$ docker exec -it ai-travel-mate-postgresql psql -U postgres -d ai_travel_bot

--Postgre script
CREATE TABLE app_user(
    user_id BIGSERIAL NOT NULL,
    first_name VARCHAR(201) NOT NULL,
    last_name VARCHAR(201) NOT NULL,
    email_id VARCHAR(201) NOT NULL,
    password VARCHAR(1000) NOT NULL,
    roles VARCHAR(500) DEFAULT ' ',
    permissions VARCHAR(500) DEFAULT ' ',
    social_login_ids VARCHAR(1000) DEFAULT ' ',
    created_by VARCHAR(100),
    created_on TIMESTAMP,
    last_updated_by VARCHAR(100),
    last_updated_on TIMESTAMP,
    PRIMARY KEY (user_id),
    CONSTRAINT app_user_emailid_uk UNIQUE (email_id)
);

-- Add table and column comments
COMMENT ON TABLE app_user IS 'maintains user accounts';
COMMENT ON COLUMN app_user.user_id IS 'Running sequence number';
COMMENT ON COLUMN app_user.email_id IS 'User email address - must be unique';
COMMENT ON COLUMN app_user.social_login_ids IS 'comma separated unique social ids. Used to map social id to app user id';
COMMENT ON COLUMN app_user.roles IS 'User roles (e.g., admin, user, moderator)';
COMMENT ON COLUMN app_user.permissions IS 'User permissions (e.g, create,read,update,delete)';

ai_travel_bot=# \d app_user
ai_travel_bot=# \q


To start the server
$ uv run app.py

Browse health check url
http://localhost:8002/health/database

SignUp (First signup will be admin. Others will be user)
POST /api/v1/auth/signup
{
  "firstName": "Balaji",
  "lastName": "Rengan",
  "email": "balajirengan@gmail.com",
  "password": "pass123"
}

SingIn
POST /api/v1/auth/signin

request
{
  "email": "balajirengan@gmail.com",
  "password": "pass123"
}

response
{
    "data": {
        "firstName": "Balaji",
        "email": "balajirengan@gmail.com",
        "roles": [
            "admin"
        ],
        "permissions": [],
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJGSVJTVF9OQU1FIjoiQmFsYWppIiwiUk9MRVMiOlsiYWRtaW4iXSwiUEVSTUlTU0lPTlMiOltdLCJzdWIiOiJiYWxhamlyZW5nYW5AZ21haWwuY29tIiwiaWF0IjoxNzYzODAzNzEwLCJleHAiOjE3NjM4MDU1MTB9.PjxOtfF6gEa5lEP9cjHzq2T8nRf7Ico2a-wuSVNzCaY"
    },
    "message": "Login successful",
    "status_code": 200
}

Getting into mongo container shell
$ docker exec -it ai-travel-mate-mongodb mongosh -u admin -p password123 --authenticationDatabase admin ai_travel_bot
ai_travel_bot> show collections;
ai_travel_bot> db.travel_collection.find({})