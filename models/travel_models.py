from datetime import date,datetime
from enum import Enum
from pydantic import BaseModel, Field,field_validator
from typing import List, Optional

class LanguageEnum(str, Enum):
    """Supported languages for the travel assistant"""
    ENGLISH = "english"
    TAMIL = "tamil"
    HINDI = "hindi"


class TravelRequest(BaseModel):
    """Request model for travel itinerary generation"""
    location: str = Field(
        ..., 
        description="Destination location (city, country, or region)",
        min_length=2,
        max_length=100,
        examples=["Tenkasi, India", "Kerala", "Mysore"]
    )
    number_of_days: int = Field(
        ..., 
        description="Number of days for the trip",
        ge=1,
        le=30
    )
    start_date: date = Field(..., description="Start date of the trip in YYYY-MM-DD format")
    preferred_language: LanguageEnum = Field(
        default=LanguageEnum.ENGLISH,
        description="Preferred language for the response"
    )
    interests: Optional[List[str]] = Field(
        default=None,
        description="Optional list of interests (e.g., history, food, nature)"
    )
    budget_level: Optional[str] = Field(
        default="medium",
        description="Budget level: budget, medium, or luxury"
    )

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v: date) -> date:
        """Ensure start date is not in the past"""
        if v < date.today():
            raise ValueError('Start date cannot be in the past')
        return v


class SightseeingPlace(BaseModel):
    """Model for individual sightseeing place"""
    name: str = Field(..., description="Name of the place")
    description: str = Field(..., description="Brief description of the place")
    category: str = Field(..., description="Category (e.g., museum, landmark, park, restaurant)")
    estimated_duration: str = Field(..., description="Estimated time to spend (e.g., '2 hours', '3-4 hours')")
    approximate_cost: Optional[str] = Field(default=None,description="Approximate cost or entry fee")
    location_details: Optional[str] = Field(default=None,description="Specific location or address")
    best_time_to_visit: Optional[str] = Field(default=None,description="Recommended time to visit",examples=["Morning", "Sunset"])


class DailyActivity(BaseModel):
    """Model for a single activity in the itinerary"""
    time: str = Field(
        ..., 
        description="Time of activity (e.g., '09:00 AM')",
        examples=["09:00 AM"]
    )
    activity: str = Field(..., description="Activity name or title")
    description: str = Field(..., description="Detailed description of the activity")
    location: str = Field(..., description="Location of the activity")
    duration: str = Field(
        ..., 
        description="Expected duration",
        examples=["2 hours"]
    )
    tips: Optional[List[str]] = Field(
        default=None,
        description="Helpful tips for this activity"
    )


class DayItinerary(BaseModel):
    """Model for a single day's itinerary"""
    day_number: int = Field(..., description="Day number in the trip", ge=1)
    date: date = Field(..., description="Date for this day")
    title: str = Field(
        ..., 
        description="Theme or title for the day",
        examples=["Exploring Ancient Rome"]
    )
    activities: List[DailyActivity] = Field(
        ..., 
        description="List of activities for the day",
        min_length=1
    )
    meals_suggestions: Optional[List[str]] = Field(
        default=None,
        description="Restaurant or meal suggestions for the day"
    )
    accommodation_note: Optional[str] = Field(
        default=None,
        description="Notes about accommodation or location to stay"
    )


class TravelResponse(BaseModel):
    """Response model for travel itinerary"""
    location: str = Field(..., description="Destination location")
    trip_duration: int = Field(..., description="Total number of days")
    start_date: date = Field(..., description="Trip start date")
    end_date: date = Field(..., description="Trip end date")
    language: str = Field(..., description="Response language")
    
    overview: str = Field(
        ..., 
        description="General overview of the trip and destination"
    )
    
    sightseeing_places: List[SightseeingPlace] = Field(
        ..., 
        description="List of recommended sightseeing places",
        min_length=1
    )
    
    itinerary: List[DayItinerary] = Field(
        ..., 
        description="Day-by-day itinerary",
        min_length=1
    )
    
    travel_tips: Optional[List[str]] = Field(
        default=None,
        description="General travel tips for the destination"
    )
    
    estimated_budget: Optional[str] = Field(
        default=None,
        description="Estimated budget range for the trip",
        examples=["$1500-2000"]
    )
    
    weather_info: Optional[str] = Field(
        default=None,
        description="Expected weather during the trip dates"
    )

class TravelRecord(BaseModel):
  email: str = Field(..., description="email of person who is going to tour")
  location: str = Field(...,description="travel destination spot")
  number_of_days: int = Field(...,description="duration of trip")
  start_date: date = Field(..., description="Start date of the trip in YYYY-MM-DD format")
  end_date: date = Field(..., description="Trip end date")

