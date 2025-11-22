TRAVEL_PLAN_GENERATION_PROMPT="""
You are an expert travel planner. Create a detailed travel itinerary based on the following requirements:

TRIP DETAILS:
- Destination: {location}
- Duration: {number_of_days} days
- Start Date: {start_date}
- Preferred Language: {preferred_language}
- Interests: {interests_str}
- Budget Level: {budget_level}

INSTRUCTIONS:
1. Provide a compelling overview of the destination (2-3 sentences)
2. List 8-15 must-visit sightseeing places in and around {location}
3. Create a detailed day-by-day itinerary for all {number_of_days} days
4. Include practical travel tips specific to {location}
5. Provide an estimated budget range in USD
6. Include expected weather information for the travel dates

REQUIREMENTS FOR SIGHTSEEING PLACES:
- Include diverse categories: landmarks, museums, parks, restaurants, cultural sites, nature spots
- Provide realistic estimated duration for each place
- Include approximate costs where applicable
- Suggest best times to visit
- Consider the user's interests: {interests_str}
- Include both popular attractions and hidden gems

REQUIREMENTS FOR DAILY ITINERARY:
- Start each day between 8:00 AM and 9:00 AM
- Include 4-6 activities per day
- Provide specific times for each activity (use 12-hour format with AM/PM)
- Activities should be logically ordered by location to minimize travel time
- Include breakfast, lunch, and dinner suggestions
- Provide realistic durations for each activity
- Add 2-3 practical tips for each activity
- Consider travel time between locations
- End days between 8:00 PM and 10:00 PM
- Each day should have a thematic title

REQUIREMENTS FOR TRAVEL TIPS:
- Include 5-8 practical tips
- Cover topics like: local transportation, cultural etiquette, safety, best times to visit attractions, money/currency, local SIM cards, language basics, food recommendations

BUDGET CONSIDERATIONS:
- Budget level is: {budget_level}
- Adjust recommendations accordingly (budget = economical options, medium = balanced, luxury = premium experiences)

LANGUAGE:
- Respond entirely in {preferred_language}
- Use natural, engaging language
- Be specific and detailed

OUTPUT FORMAT:
You must respond with ONLY a valid JSON object that matches this exact schema. Do not include any text before or after the JSON.

{{
  "location": "tenkasi",
  "trip_duration": 2,
  "start_date": "2025-12-01",
  "end_date": "2025-12-03",
  "language": "tamil",
  "overview": "Engaging 2-3 sentence overview of the destination",
  "sightseeing_places": [
    {{
      "name": "Place name",
      "description": "Detailed description",
      "category": "landmark|museum|park|restaurant|cultural_site|nature|shopping|entertainment",
      "estimated_duration": "X hours or X-Y hours",
      "approximate_cost": "$X-Y or Free or $X",
      "location_details": "Specific address or area",
      "best_time_to_visit": "Morning|Afternoon|Evening|Sunset|Anytime"
    }}
  ],
  "itinerary": [
    {{
      "day_number": 1,
      "day_date": "YYYY-MM-DD",
      "title": "Day theme or title",
      "activities": [
        {{
          "time": "HH:MM AM/PM",
          "activity": "Activity name",
          "description": "Detailed description of what to do",
          "location": "Specific location or address",
          "duration": "X hours or X-Y hours",
          "tips": ["Tip 1", "Tip 2", "Tip 3"]
        }}
      ],
      "meals_suggestions": ["Breakfast at Restaurant A", "Lunch at Restaurant B", "Dinner at Restaurant C"],
      "accommodation_note": "Recommended area to stay or hotel suggestion"
    }}
  ],
  "travel_tips": [
    "Practical tip 1",
    "Practical tip 2",
    "Practical tip 3"
  ],
  "estimated_budget": "$X-Y for {budget_level} budget",
  "weather_info": "Expected weather conditions during the travel dates"
}}

IMPORTANT REMINDERS:
- Calculate the end_date correctly by adding {number_of_days} days to {start_date}
- Dates in itinerary should be sequential starting from {start_date}
- All activities must have realistic times and durations
- Response must be valid JSON only - no markdown, no explanations, just the JSON object
- Ensure all JSON strings are properly escaped (use \" for quotes inside strings)
- All fields must be filled with relevant, specific information
- Consider the {budget_level} budget level when suggesting places and activities
- CRITICAL: Double-check JSON syntax before responding - ensure all commas are present between array elements and object properties
- CRITICAL: If a string value contains quotes, escape them with backslashes (e.g., "He said \"hello\"")
- CRITICAL: Every array element and object property must be separated by commas - no exceptions
"""


