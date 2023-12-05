from datetime import datetime
from collections import deque
class Client:
    def __init__(self, name):
        self.name = name

    def notify(self, msg):
        print(f"{self.name} got message: {msg}")

class Meeting:
    def __init__(self, start_time, end_time, participants):
        self.start_time = start_time
        self.end_time = end_time
        self.participants = participants
    
    def notify(self, msg):
        for member in self.participants:
            member.notify(msg)
    
class Meeting_Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.scheduled_meetings_timing_in_this_room = []
    
    def is_available(self, meeting):
        for scheduled_meeting_timing in self.scheduled_meetings_timing_in_this_room:
            if scheduled_meeting_timing.end_time > meeting.start_time and meeting.end_time > scheduled_meeting_timing.start_time:
                return False
        return True
    
    def book_meeting(self, meeting):
        if self.is_available(meeting):
           meeting.notify(f"Meeting is scheduled in Room {self.room_number} from {meeting.start_time} to {meeting.end_time}")
           self.scheduled_meetings_timing_in_this_room.append(meeting)
           return True
        return False

class Meeting_Scheduler:
    def __init__(self, num_rooms):
        self.num_rooms = num_rooms
        self.meeting_rooms = [Meeting_Room(i) for i in range(1, num_rooms+1)]
        self.meeting_history = deque(maxlen=20)
    
    def schedule_meeting(self, start_time, end_time, participants):
        meeting = Meeting(start_time, end_time, participants)
        for room in self.meeting_rooms:
            if room.is_available(meeting):
                room.book_meeting(meeting)
                self.meeting_history.append(meeting)
                return (f"Meeting booked in Room {room.room_number} from {start_time} to {end_time}")
        return (f"No available meeting rooms for the given time")

    def get_meeting_history(self):
        return list(self.meeting_history)

class Meeting_Scheduler_Api:
    def __init__(self, meeting_scheduler):
        self.meeting_scheduler = meeting_scheduler
    
    def book_meeting(self, start_time, end_time, participants):
        return self.meeting_scheduler.schedule_meeting(start_time, end_time, participants)
    
    def get_meeting_history(self):
        return self.meeting_scheduler.get_meeting_history()
    
if __name__ == '__main__':

    num_of_rooms = 2
    meeting_scheduler = Meeting_Scheduler(num_of_rooms)
    api = Meeting_Scheduler_Api(meeting_scheduler)
    Alice = Client("Alice")
    Bob = Client("Bob")
    Charlie = Client("Charlie")
    David = Client("David")
    (api.book_meeting(datetime(2023, 12, 5, 10, 0), datetime(2023, 12, 5, 12, 0), [Alice, Bob]))
    (api.book_meeting(datetime(2023, 12, 5, 11, 0), datetime(2023, 12, 5, 13, 0), [Charlie, David]))
    # print(api.get_meeting_history())
   
# from datetime import datetime, timedelta
# from collections import deque

# class Meeting:
#     def __init__(self, start_time, end_time, participants):
#         self.start_time = start_time
#         self.end_time = end_time
#         self.participants = participants

# class MeetingRoom:
#     def __init__(self, room_number):
#         self.room_number = room_number
#         self.schedule = []

#     def is_available(self, start_time, end_time):
#         for meeting in self.schedule:
#             if start_time < meeting.end_time and end_time > meeting.start_time:
#                 return False
#         return True

#     def book_meeting(self, meeting):
#         if self.is_available(meeting.start_time, meeting.end_time):
#             self.schedule.append(meeting)
#             return True
#         return False

# class MeetingScheduler:
#     def __init__(self, num_rooms):
#         self.meeting_rooms = [MeetingRoom(room_number=i) for i in range(1, num_rooms + 1)]
#         self.meeting_history = deque(maxlen=20)

#     def schedule_meeting(self, start_time, end_time, participants):
#         meeting = Meeting(start_time, end_time, participants)
#         for room in self.meeting_rooms:
#             if room.is_available(start_time, end_time):
#                 room.book_meeting(meeting)
#                 self.meeting_history.append(meeting)
#                 return f"Meeting booked in Room {room.room_number}"

#         return "No available meeting rooms for the given time"

#     def get_meeting_history(self):
#         return list(self.meeting_history)

# class MeetingSchedulerAPI:
#     def __init__(self, meeting_scheduler):
#         self.meeting_scheduler = meeting_scheduler

#     def book_meeting(self, start_time, end_time, participants):
#         return self.meeting_scheduler.schedule_meeting(start_time, end_time, participants)

#     def get_meeting_history(self):
#         return self.meeting_scheduler.get_meeting_history()

# # Example Usage
# if __name__ == "__main__":
#     num_rooms = 3
#     scheduler = MeetingScheduler(num_rooms)
#     api = MeetingSchedulerAPI(scheduler)

#     print(api.book_meeting(datetime(2023, 12, 5, 10, 0), datetime(2023, 12, 5, 12, 0), ["Alice", "Bob"]))
#     print(api.book_meeting(datetime(2023, 12, 5, 11, 0), datetime(2023, 12, 5, 13, 0), ["Charlie", "David"]))

#     print(api.get_meeting_history())

       
