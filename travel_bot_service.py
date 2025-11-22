from datetime import datetime, timezone
from models.api_responses import SuccessResponse
from models.status_code import sc
from models.travel_models import *
from typing import Dict, Any, List
from utils.logger import logger
from utils.mongo_db_manager import mongodb_manager
from mongo_collection_names import CollectionNames
from utils.config import settings
from travel_bot_exception import TravelBotException
from bson import ObjectId
from bson.errors import InvalidId
import csv
import io
from utils import llm_manager, pdf_manager


class TravelBotService:

    async def generate_travel_plan(self,email: str,travel_request: TravelRequest) -> SuccessResponse[TravelResponse]:
      try:
          logger.info(
              f"Generating travel plan for email='{email}', "
              f"location='{travel_request.location}', "
              f"days={travel_request.number_of_days}"
          )

          # Call LLM manager to generate the travel plan
          travel_response: TravelResponse = await llm_manager.generate_travel_plan(travel_request)

          logger.info(
              f"Successfully generated travel plan for email='{email}', "
              f"location='{travel_request.location}'"
          )

          # Persist request/response for later retrieval/analytics
          await self._persist_travel_data(email, travel_request, travel_response)

          return SuccessResponse(data=travel_response, status_code=sc.SUCCESS)

      except TravelBotException:
          # Bubble up domain-specific exceptions unchanged
          raise
      except Exception as exc:
          raise TravelBotException(
              message="Failed to generate travel plan",
              error_code=sc.INTERNAL_SERVER_ERROR,
              original_exception=exc,
          )

    async def _persist_travel_data(self, email:str,travel_request: TravelRequest, travel_response: TravelResponse) -> None:
        travel_collection = mongodb_manager.get_collection(CollectionNames.TRAVEL_COLLECTION)
        await travel_collection.insert_one({
            "email": email,
            "request" : travel_request.model_dump(exclude_none=True),
            "response" : travel_response.model_dump(exclude_none=True)
          })
    
    async def download_travel_plan(self, email: str) -> bytes:
        """
        Fetch the stored travel request/response for the given email and
        return a generated PDF as raw bytes.
        """
        try:
            logger.info(f"Downloading travel plan PDF for email='{email}'")

            travel_collection = mongodb_manager.get_collection(CollectionNames.TRAVEL_COLLECTION)
            doc = await travel_collection.find_one({"email": email})

            if not doc:
                raise TravelBotException(
                    message="No travel plan found for the given email",
                    error_code=sc.ENTITY_NOT_FOUND,
                    details={"email": email}
                )

            request_data = doc.get("request")
            response_data = doc.get("response")

            travel_request = TravelRequest(**request_data)
            travel_response = TravelResponse(**response_data)

            pdf_bytes = pdf_manager.generate_travel_plan_pdf(travel_request, travel_response)
            return pdf_bytes

        except TravelBotException:
            # Propagate domain error as-is
            raise
        except Exception as exc:
            raise TravelBotException(
                message="Failed to generate travel plan PDF",
                error_code=sc.INTERNAL_SERVER_ERROR,
                original_exception=exc,
                details={"email": email}
            )

    async def get_all_travel_plans(self) -> SuccessResponse[List[TravelRecord]]:

        try:
            travel_collection = mongodb_manager.get_collection(CollectionNames.TRAVEL_COLLECTION)

            cursor = travel_collection.find()
            travel_records: List[TravelRecord] = []

            async for doc in cursor:
              request_data = doc.get("request", {})
              response_data = doc.get("response", {})

              record = TravelRecord(
                  email=doc.get("email"),
                  location=request_data.get("location"),
                  number_of_days=request_data.get("number_of_days"),
                  start_date=request_data.get("start_date"),
                  end_date=response_data.get("end_date")
              )
              travel_records.append(record)

            return SuccessResponse(data=travel_records, status_code=sc.SUCCESS)

        except Exception as exc:
            raise TravelBotException(
                message="Failed to fetch travel plans",
                error_code=sc.INTERNAL_SERVER_ERROR,
                original_exception=exc
            )


travelbot_service = TravelBotService()
