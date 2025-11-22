from travel_bot_exception import TravelBotException
from models.status_code import sc
from typing import Optional

class JwtException(TravelBotException):
    def __init__(
        self,
        message: str,
        original_exception: Optional[Exception] = None
    ):
        super().__init__(message=message,
                         error_code=sc.FORBIDDEN,
                         original_exception=original_exception)
