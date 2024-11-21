
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, time
from sqlalchemy import and_
from models import WeeklyAvailability, SpecificAvailability, ScheduledEvent
import pytz
from utils import convert_to_timezone, DateTimeSegmentManager

def get_common_availability(db: Session, input):
    """
    Calculates the common availability of multiple users over a given date range.

    This function handles time zone conversion, overlapping availability,
    and unavailable segments for each user in the input. The result is a
    dictionary of unavailable segments for each date.

    Args:
    db (Session): Database session object for querying availability data.
    input: Input object containing the following:
        - start_date: Start date of the range (timezone aware).
        - end_date: End date of the range (timezone aware).
        - timezone: The timezone to which dates should be converted.
        - user_ids: List of user IDs for which availability is calculated.

    Returns:
    dict: A dictionary with dates as keys and unavailable time segments as values.
    """

    start_date = convert_to_timezone(input.start_date, input.timezone)
    end_date = convert_to_timezone(input.end_date, input.timezone)

    manager = DateTimeSegmentManager(time(0,0,0), time(23,59,59))

    unavailable = {}
    
    for user_id in input.user_ids:
        db_availabilities = db.query(WeeklyAvailability).filter(WeeklyAvailability.user_id == user_id).all()
        if not db_availabilities:
            # pass
            raise HTTPException(status_code=404, detail="No availability found for this user.")
        
        db_specific_availabilities = db.query(SpecificAvailability).filter(SpecificAvailability.user_id == user_id).all()
        specific_availability_dict= {}
        if not db_specific_availabilities:
            pass
        else:
            for availability in db_specific_availabilities:
                try:
                    _ = specific_availability_dict[availability.date] 
                except:
                    specific_availability_dict[availability.date] = []
                specific_availability_dict[availability.date].append({"start_time": availability.start_time, "end_time": availability.end_time })
        

        


        for day_offset in range((end_date-start_date).days + 1):
            current_date = start_date + timedelta (days=day_offset)
            weekday = current_date.weekday()
            manager = DateTimeSegmentManager(time(0,0,0), time(23,59,59))
            try:
                _ = unavailable[current_date]
            except:
                unavailable[current_date] = []
                
                
            if current_date in specific_availability_dict:
                for availability in specific_availability_dict[current_date]:
                    manager.add_segment(availability["start_time"], availability["end_time"])
            else:
                for availability in db_availabilities:
                    if (availability.day_of_week == weekday):
                        # pass
                        manager.add_segment(availability.start_time, availability.end_time)
            for free_seg in manager.get_unavailable_segments():
                unavailable[current_date].append(free_seg)
    
    output_dict = {}
    for day_offset in range((end_date-start_date).days + 1):
            current_date = start_date + timedelta (days=day_offset)
            weekday = current_date.weekday()
            manager = DateTimeSegmentManager(time(0,0,0), time(23,59,59))
            try:
                _ = output_dict[current_date]
            except:
                output_dict[current_date] = []

            for seg in unavailable[current_date]:
                manager.add_segment(seg[0], seg[1])

            for free_seg in manager.get_unavailable_segments():
                output_dict[current_date].append(free_seg)

    return output_dict
