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

Create Travel Plan (requires user role)
POST /api/v1/travelbot/plan
request
{
    "location": "Italy",
    "number_of_days": 2,
    "start_date": "2026-12-25",
    "preferred_language" : "english"
}

response
{
  "data": {
      "location": "Italy",
      "trip_duration": 2,
      "start_date": "2026-12-25T00:00:00",
      "end_date": "2026-12-27T00:00:00",
      "language": "ENGLISH",
      "overview": "Italy, a country rich in history, art, and gastronomy, offers travelers a glimpse into the past with its ancient ruins, Renaissance art, and charming villages. From the bustling streets of Rome to the romantic canals of Venice, Italy is a destination that captivates the heart and soul.",
      "sightseeing_places": [
          {
              "name": "Colosseum",
              "description": "An iconic symbol of Imperial Rome, the Colosseum is a must-visit landmark where gladiators once fought for glory.",
              "category": "landmark",
              "estimated_duration": "2-3 hours",
              "approximate_cost": "$18-25",
              "location_details": "Piazza del Colosseo, 00184 Rome, Italy",
              "best_time_to_visit": "Morning"
          },
          {
              "name": "Vatican Museums",
              "description": "Home to a vast collection of art and historical artifacts, including the Sistine Chapel's ceiling painted by Michelangelo.",
              "category": "museum",
              "estimated_duration": "3-4 hours",
              "approximate_cost": "$21",
              "location_details": "Viale Vaticano, 00165 Rome, Italy",
              "best_time_to_visit": "Morning"
          },
          {
              "name": "Trevi Fountain",
              "description": "A stunning Baroque fountain where visitors toss coins to ensure their return to Rome.",
              "category": "landmark",
              "estimated_duration": "30 minutes",
              "approximate_cost": "Free",
              "location_details": "Piazza di Trevi, 00187 Rome, Italy",
              "best_time_to_visit": "Evening"
          },
          {
              "name": "Pantheon",
              "description": "A former Roman temple, now a church, known for its impressive dome and oculus.",
              "category": "cultural_site",
              "estimated_duration": "1 hour",
              "approximate_cost": "Free",
              "location_details": "Piazza della Rotonda, 00186 Rome, Italy",
              "best_time_to_visit": "Afternoon"
          },
          {
              "name": "Piazza Navona",
              "description": "A lively square featuring beautiful fountains and architecture, perfect for people-watching.",
              "category": "cultural_site",
              "estimated_duration": "1-2 hours",
              "approximate_cost": "Free",
              "location_details": "Piazza Navona, 00186 Rome, Italy",
              "best_time_to_visit": "Afternoon"
          },
          {
              "name": "Galleria Borghese",
              "description": "An art gallery housing a significant collection of sculptures and paintings by masters like Caravaggio and Bernini.",
              "category": "museum",
              "estimated_duration": "2-3 hours",
              "approximate_cost": "$15-20",
              "location_details": "Piazzale Scipione Borghese, 5, 00197 Rome, Italy",
              "best_time_to_visit": "Morning"
          },
          {
              "name": "Roman Forum",
              "description": "The heart of ancient Rome, this site offers a glimpse into the political, social, and economic life of the empire.",
              "category": "landmark",
              "estimated_duration": "1-2 hours",
              "approximate_cost": "$16-20",
              "location_details": "Via della Salara Vecchia, 5/6, 00186 Rome, Italy",
              "best_time_to_visit": "Morning"
          },
          {
              "name": "Trastevere",
              "description": "A charming neighborhood known for its narrow streets, vibrant nightlife, and authentic Roman cuisine.",
              "category": "cultural_site",
              "estimated_duration": "2-3 hours",
              "approximate_cost": "Varies",
              "location_details": "Trastevere, Rome, Italy",
              "best_time_to_visit": "Evening"
          }
      ],
      "itinerary": [
          {
              "day_number": 1,
              "day_date": "2026-12-25T00:00:00",
              "title": "Exploring Ancient Rome",
              "activities": [
                  {
                      "time": "9:00 AM",
                      "activity": "Visit the Colosseum",
                      "description": "Explore the iconic Colosseum, learning about its history and significance in Roman culture.",
                      "location": "Piazza del Colosseo, 00184 Rome, Italy",
                      "duration": "2-3 hours",
                      "tips": [
                          "Book tickets in advance to skip the line.",
                          "Wear comfortable shoes for walking.",
                          "Consider a guided tour for in-depth information."
                      ]
                  },
                  {
                      "time": "12:00 PM",
                      "activity": "Lunch at Trattoria Luzzi",
                      "description": "Enjoy a traditional Italian lunch at a local trattoria near the Colosseum.",
                      "location": "Via di San Giovanni in Laterano, 88, 00184 Rome, Italy",
                      "duration": "1 hour",
                      "tips": [
                          "Try the pasta dishes, they are highly recommended.",
                          "Arrive early to avoid the lunch rush.",
                          "Cash is preferred at many local eateries."
                      ]
                  },
                  {
                      "time": "1:30 PM",
                      "activity": "Explore the Roman Forum",
                      "description": "Walk through the ruins of the Roman Forum, the center of ancient Roman life.",
                      "location": "Via della Salara Vecchia, 5/6, 00186 Rome, Italy",
                      "duration": "1-2 hours",
                      "tips": [
                          "Bring a hat and sunscreen if it's sunny.",
                          "Download a map or guide app for better navigation.",
                          "Stay hydrated as you'll be walking a lot."
                      ]
                  },
                  {
                      "time": "3:30 PM",
                      "activity": "Visit the Pantheon",
                      "description": "Marvel at the architectural wonder of the Pantheon, with its impressive dome and oculus.",
                      "location": "Piazza della Rotonda, 00186 Rome, Italy",
                      "duration": "1 hour",
                      "tips": [
                          "Check the opening hours as they may vary on holidays.",
                          "Respect the silence inside as it's a place of worship.",
                          "Photography is allowed, but be mindful of others."
                      ]
                  },
                  {
                      "time": "5:00 PM",
                      "activity": "Relax at Piazza Navona",
                      "description": "Stroll around Piazza Navona, enjoying the fountains, street performers, and vibrant atmosphere.",
                      "location": "Piazza Navona, 00186 Rome, Italy",
                      "duration": "1-2 hours",
                      "tips": [
                          "Watch out for pickpockets in crowded areas.",
                          "Enjoy a gelato from one of the nearby shops.",
                          "Take time to admire the Fountain of the Four Rivers."
                      ]
                  },
                  {
                      "time": "7:00 PM",
                      "activity": "Dinner at Osteria da Fortunata",
                      "description": "Dine at a popular Roman osteria known for its homemade pasta and cozy atmosphere.",
                      "location": "Via del Pellegrino, 11, 00186 Rome, Italy",
                      "duration": "1-2 hours",
                      "tips": [
                          "Reservations are recommended.",
                          "Try the cacio e pepe, a Roman specialty.",
                          "Enjoy a glass of local wine with your meal."
                      ]
                  }
              ],
              "meals_suggestions": [
                  "Breakfast at Roscioli Caffè",
                  "Lunch at Trattoria Luzzi",
                  "Dinner at Osteria da Fortunata"
              ],
              "accommodation_note": "Stay in the Centro Storico area for easy access to major attractions."
          },
          {
              "day_number": 2,
              "day_date": "2026-12-26T00:00:00",
              "title": "Art and Culture in Rome",
              "activities": [
                  {
                      "time": "8:30 AM",
                      "activity": "Visit the Vatican Museums",
                      "description": "Discover the vast art collections of the Vatican Museums, including the Sistine Chapel.",
                      "location": "Viale Vaticano, 00165 Rome, Italy",
                      "duration": "3-4 hours",
                      "tips": [
                          "Purchase tickets online to avoid long queues.",
                          "Dress modestly as it's a religious site.",
                          "Consider an audio guide for detailed insights."
                      ]
                  },
                  {
                      "time": "12:30 PM",
                      "activity": "Lunch at Ristorante dei Musei",
                      "description": "Enjoy a leisurely lunch at a restaurant near the Vatican, offering Italian classics.",
                      "location": "Via Santamaura, 5, 00192 Rome, Italy",
                      "duration": "1 hour",
                      "tips": [
                          "Try the seafood pasta for a delightful meal.",
                          "Outdoor seating is available for a pleasant dining experience.",
                          "Service charge may be included in the bill."
                      ]
                  },
                  {
                      "time": "2:00 PM",
                      "activity": "Explore Galleria Borghese",
                      "description": "Admire the art and sculptures at Galleria Borghese, set in the beautiful Villa Borghese gardens.",
                      "location": "Piazzale Scipione Borghese, 5, 00197 Rome, Italy",
                      "duration": "2-3 hours",
                      "tips": [
                          "Book your entry time in advance as slots fill up quickly.",
                          "Photography is not allowed inside the gallery.",
                          "Take a stroll in the gardens after your visit."
                      ]
                  },
                  {
                      "time": "5:00 PM",
                      "activity": "Visit Trevi Fountain",
                      "description": "Toss a coin into the Trevi Fountain, ensuring your return to Rome.",
                      "location": "Piazza di Trevi, 00187 Rome, Italy",
                      "duration": "30 minutes",
                      "tips": [
                          "Visit in the evening for a magical view with the lights.",
                          "Be cautious of street vendors selling souvenirs.",
                          "Capture the moment with a photo."
                      ]
                  },
                  {
                      "time": "6:30 PM",
                      "activity": "Explore Trastevere",
                      "description": "Wander through the charming streets of Trastevere, experiencing its lively atmosphere and local culture.",
                      "location": "Trastevere, Rome, Italy",
                      "duration": "2-3 hours",
                      "tips": [
                          "Wear comfortable shoes for walking on cobblestone streets.",
                          "Try a slice of pizza bianca from a local bakery.",
                          "Enjoy a drink at a local bar to end the day."
                      ]
                  }
              ],
              "meals_suggestions": [
                  "Breakfast at Bar del Cappuccino",
                  "Lunch at Ristorante dei Musei",
                  "Dinner in Trastevere"
              ],
              "accommodation_note": "Consider staying in Trastevere for a more authentic Roman experience."
          }
      ],
      "travel_tips": [
          "Public transportation is efficient; consider getting a Roma Pass for unlimited travel and discounts.",
          "Learn a few basic Italian phrases; locals appreciate the effort.",
          "Keep an eye on your belongings, especially in crowded tourist areas.",
          "Most restaurants include a service charge; tipping is optional but appreciated.",
          "Purchase tickets for major attractions online to save time.",
          "Consider using an eSIM or local SIM card for internet access.",
          "Try local specialties like gelato, pizza, and pasta for an authentic taste of Italy."
      ],
      "estimated_budget": "$500-700 for medium budget",
      "weather_info": "Expect cool, mild weather with average temperatures ranging from 40°F to 55°F (4°C to 13°C)."
  },
  "status_code": 200
}

Get all travel plans (requires admin role)

GET /api/v1/travelbot/plan/all

response
{
    "data": [
        {
            "email": "balajirengan@gmail.com",
            "location": "Singapore",
            "number_of_days": 2,
            "start_date": "2025-12-25T00:00:00",
            "end_date": "2025-12-27T00:00:00"
        },
        {
            "email": "balajirengan@gmail.com",
            "location": "Italy",
            "number_of_days": 2,
            "start_date": "2026-12-25T00:00:00",
            "end_date": "2026-12-27T00:00:00"
        }
    ],
    "status_code": 200
}


Download Travel Plan pdf (requires user role)
GET /api/v1/travelbot/plan

Getting into mongo container shell
$ docker exec -it ai-travel-mate-mongodb mongosh -u admin -p password123 --authenticationDatabase admin ai_travel_bot
ai_travel_bot> show collections;
ai_travel_bot> db.travel_collection.find({})