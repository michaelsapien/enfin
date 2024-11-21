import datetime
from typing import List, Tuple, Optional
import pytz

# Utility function to convert times to a common timezone
def convert_to_timezone(input_time, timezone_str):
    """Converts a naive datetime to a timezone-aware datetime."""
    local_tz = pytz.timezone(timezone_str)
    # return input_time.astimezone(local_tz)
    return input_time

class DateTimeSegmentManager:
    """
    A comprehensive manager for datetime segments with global start and stop.
    """
    
    def __init__(self, global_start: datetime.datetime, global_stop: datetime.datetime):
        """
        Initialize the segment manager with a global time range.
        
        Args:
            global_start (datetime.datetime): The absolute start of the time range
            global_stop (datetime.datetime): The absolute end of the time range
        """
        if global_start >= global_stop:
            raise ValueError("Global start must be before global stop")
        
        self.global_start = global_start
        self.global_stop = global_stop
        self.segments = []
    
    def add_segment(self, start: datetime.datetime, end: datetime.datetime):
        """
        Add a segment, ensuring it's within the global time range.
        
        Args:
            start (datetime.datetime): Start of the segment
            end (datetime.datetime): End of the segment
        """
        # Clip segment to global range
        segment_start = max(start, self.global_start)
        segment_end = min(end, self.global_stop)
        
        if segment_start < segment_end:
            self.segments.append((segment_start, segment_end))
        
        # Sort segments after adding
        self.segments.sort(key=lambda x: x[0])
    
    def get_unavailable_segments(self) -> List[Tuple[datetime.datetime, datetime.datetime]]:
        """
        Compute the free (unoccupied) segments within the global range.
        
        Returns:
            List of tuples representing free time segments
        """
        # If no segments, entire range is free
        if not self.segments:
            return [(self.global_start, self.global_stop)]
        
        free_segments = []
        current = self.global_start
        
        for start, end in self.segments:
            # Add free segment before this segment if exists
            if current < start:
                free_segments.append((current, start))
            
            # Move current to the end of this segment
            current = max(current, end)
        
        # Add final free segment if any remains
        if current < self.global_stop:
            free_segments.append((current, self.global_stop))
        
        return free_segments
    
       
    
    
 

def main():
    # Define global time range
    dt1 = datetime.datetime(2024, 1, 1, 0, 0)
    dt2 = datetime.datetime(2024, 1, 20, 0, 0)
    
    # Create segment manager
    manager = DateTimeSegmentManager(dt1, dt2)
    
    # Add multiple segments with various overlaps
    segments_to_add = [
        (datetime.datetime(2024, 1, 2), datetime.datetime(2024, 1, 5)),
        (datetime.datetime(2024, 1, 3), datetime.datetime(2024, 1, 7)),
        (datetime.datetime(2024, 1, 6), datetime.datetime(2024, 1, 10)),
        (datetime.datetime(2024, 1, 15), datetime.datetime(2024, 1, 18))
    ]
    
    # Add segments
    for start, end in segments_to_add:
        manager.add_segment(start, end)
    
    
    
    unavailable = []
    for free_seg in manager.get_unavailable_segments():
        # print(f"{free_seg[0]} to {free_seg[1]}")
        unavailable.append([free_seg[0], free_seg[1]])
    

    manager1 = DateTimeSegmentManager(dt1, dt2)

    for f2 in unavailable :
        # print(f2)
        manager1.add_segment(f2[0], f2[1])
        # print(f2[0], f2[1])
    

    

if __name__ == "__main__":
    main()