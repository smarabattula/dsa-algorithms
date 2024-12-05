# TimeSlot: starttime: TimeStamp, endtime: TimeStamp
# User: id, name, meetings: list[meeting]
# Meeting: id, slot: TimeSlot, attendees: List[User]
# Application: meetings: List[Meeting], users: List[user]

"""
Design Patterns used: Singleton, Observer
"""
from datetime import datetime
from typing import Set, List

class TimeSlot:
    def __init__(self,startTime: datetime, endTime: datetime):
        self._startTime = startTime
        self._endTime = endTime

    def overlaps(self, slot2: 'TimeSlot') -> bool: # TimeSlot as forward reference
        if (slot2._startTime <= self._startTime <= slot2._endTime) or (self._startTime <= slot2._startTime <=self._endTime):
            return True
        else:
            return False

class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.calendar: Set[Meeting] = set()

    def view_calendar(self):
        for meeting in self.calendar:
            print(self.calendar[meeting])

    def add_meeting(self, meeting: 'Meeting'):
        self.calendar.add(meeting)
        return

    def delete_meeting(self, meeting: 'Meeting'):
        self.calendar.remove(meeting)

class Meeting:
    def __init__(self, id, timeSlot : TimeSlot, attendees: List[User]):
        self.id = id
        self.timeSlot: TimeSlot = timeSlot
        self.attendees: List[User] = attendees

class MeetingScheduler:
    _instance = None

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def _is_feasible(self, meeting: Meeting) -> bool:
        slot1 = meeting.timeSlot
        users = meeting.attendees
        for user in users:
            for user_meeting in user.calendar:
                slot2 = user_meeting.timeSlot
                if slot1.overlaps(slot2):
                    return False

        return True

    def create_meeting(self, meeting: Meeting) -> bool:
        if not self._is_feasible(meeting):
            return False

        users = meeting.attendees
        for user in users:
            user.add_meeting(meeting)

        return True

    def remove_meeting(self, meeting: Meeting):
        users = meeting.attendees
        for user in users:
            user.delete_meeting(meeting)
        return

    def update_meeting(self, old_meeting: Meeting, new_meeting: Meeting):
        users = new_meeting.attendees
        slot1 = new_meeting.timeSlot
        for user in users:
            for meeting in user.calendar:
                slot2 = meeting.timeSlot
                if meeting.id != old_meeting.id and slot1.overlaps(slot2):
                    return False

        self.remove_meeting(old_meeting)
        self.create_meeting(new_meeting)

        return True
