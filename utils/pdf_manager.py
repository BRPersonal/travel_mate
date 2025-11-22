from io import BytesIO
from typing import List

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from models.travel_models import TravelRequest, TravelResponse, DayItinerary, DailyActivity, SightseeingPlace
from utils.logger import logger


def _draw_wrapped_text(c: canvas.Canvas, text: str, x: float, y: float, max_width: float, line_height: float) -> float:
    """
    Draw text with simple word wrapping. Returns the new y-position
    after drawing the text block.
    """
    if not text:
        return y

    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if c.stringWidth(test_line) <= max_width:
            line = test_line
        else:
            c.drawString(x, y, line)
            y -= line_height
            line = word

    if line:
        c.drawString(x, y, line)
        y -= line_height

    return y


def generate_travel_plan_pdf(travel_request: TravelRequest, travel_response: TravelResponse) -> bytes:
    """
    Generate a PDF file (as bytes) for the given travel request/response.
    """
    logger.info(
        f"Generating travel plan PDF for email='{getattr(travel_request, 'email', 'N/A')}', "
        f"location='{travel_request.location}', days={travel_request.number_of_days}"
    )

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin_x = 2 * cm
    max_text_width = width - 2 * margin_x
    y = height - 2 * cm
    line_height = 14

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin_x, y, f"Travel Plan - {travel_response.location}")
    y -= 24

    # Basic info
    c.setFont("Helvetica", 12)
    y = _draw_wrapped_text(
        c,
        f"Trip Duration: {travel_response.trip_duration} days "
        f"({travel_response.start_date} to {travel_response.end_date})",
        margin_x,
        y,
        max_text_width,
        line_height,
    )
    y = _draw_wrapped_text(
        c,
        f"Language: {travel_response.language}",
        margin_x,
        y,
        max_text_width,
        line_height,
    )

    y -= line_height

    # Overview
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_x, y, "Overview")
    y -= 18
    c.setFont("Helvetica", 12)
    y = _draw_wrapped_text(c, travel_response.overview, margin_x, y, max_text_width, line_height)
    y -= line_height

    # Sightseeing places
    if travel_response.sightseeing_places:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin_x, y, "Sightseeing Places")
        y -= 18
        c.setFont("Helvetica", 12)

        for place in travel_response.sightseeing_places:
            if y < 4 * cm:
                c.showPage()
                y = height - 2 * cm
                c.setFont("Helvetica", 12)

            y = _draw_wrapped_text(c, f"- {place.name} ({place.category})", margin_x, y, max_text_width, line_height)
            if place.description:
                y = _draw_wrapped_text(c, f"  {place.description}", margin_x + 10, y, max_text_width - 10, line_height)
            if place.estimated_duration:
                y = _draw_wrapped_text(
                    c,
                    f"  Duration: {place.estimated_duration}",
                    margin_x + 10,
                    y,
                    max_text_width - 10,
                    line_height,
                )
            if place.approximate_cost:
                y = _draw_wrapped_text(
                    c,
                    f"  Approx. Cost: {place.approximate_cost}",
                    margin_x + 10,
                    y,
                    max_text_width - 10,
                    line_height,
                )
            y -= line_height / 2

    # Day-by-day itinerary
    if travel_response.itinerary:
        for day in travel_response.itinerary:
            if y < 5 * cm:
                c.showPage()
                y = height - 2 * cm

            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin_x, y, f"Day {day.day_number} - {day.day_date}: {day.title}")
            y -= 18

            c.setFont("Helvetica", 12)
            for activity in day.activities:
                if y < 4 * cm:
                    c.showPage()
                    y = height - 2 * cm
                    c.setFont("Helvetica", 12)

                title_line = f"{activity.time} - {activity.activity} @ {activity.location}"
                y = _draw_wrapped_text(c, title_line, margin_x, y, max_text_width, line_height)
                y = _draw_wrapped_text(
                    c,
                    activity.description,
                    margin_x + 10,
                    y,
                    max_text_width - 10,
                    line_height,
                )
                y = _draw_wrapped_text(
                    c,
                    f"Duration: {activity.duration}",
                    margin_x + 10,
                    y,
                    max_text_width - 10,
                    line_height,
                )
                if activity.tips:
                    for tip in activity.tips:
                        y = _draw_wrapped_text(
                            c,
                            f"Tip: {tip}",
                            margin_x + 10,
                            y,
                            max_text_width - 10,
                            line_height,
                        )
                y -= line_height / 2

            if day.meals_suggestions:
                if y < 4 * cm:
                    c.showPage()
                    y = height - 2 * cm
                y = _draw_wrapped_text(
                    c,
                    "Meals: " + "; ".join(day.meals_suggestions),
                    margin_x + 10,
                    y,
                    max_text_width - 10,
                    line_height,
                )

            if day.accommodation_note:
                if y < 4 * cm:
                    c.showPage()
                    y = height - 2 * cm
                y = _draw_wrapped_text(
                    c,
                    "Accommodation: " + day.accommodation_note,
                    margin_x + 10,
                    y,
                    max_text_width - 10,
                    line_height,
                )

            y -= line_height

    # Additional info
    if travel_response.travel_tips:
        if y < 4 * cm:
            c.showPage()
            y = height - 2 * cm
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin_x, y, "Travel Tips")
        y -= 18
        c.setFont("Helvetica", 12)
        for tip in travel_response.travel_tips:
            y = _draw_wrapped_text(c, f"- {tip}", margin_x, y, max_text_width, line_height)

    if travel_response.estimated_budget:
        if y < 3 * cm:
            c.showPage()
            y = height - 2 * cm
        y -= line_height
        c.setFont("Helvetica-Bold", 12)
        y = _draw_wrapped_text(
            c,
            f"Estimated Budget: {travel_response.estimated_budget}",
            margin_x,
            y,
            max_text_width,
            line_height,
        )

    if travel_response.weather_info:
        if y < 3 * cm:
            c.showPage()
            y = height - 2 * cm
        c.setFont("Helvetica-Bold", 12)
        y = _draw_wrapped_text(
            c,
            f"Weather Info: {travel_response.weather_info}",
            margin_x,
            y,
            max_text_width,
            line_height,
        )

    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    logger.info(f"Travel plan PDF generated successfully, size={len(pdf_bytes)} bytes")
    return pdf_bytes

