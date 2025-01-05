from datetime import datetime, timedelta
from .field import Field
from .errorhandler import input_error

class Birthday(Field):
  __DATE_FORMAT = "%d.%m.%Y"
  
  def __init__(self, value):
      checked = self.check_data(value)
      super().__init__(checked)
      
  @input_error
  def check_data(self, value):
      try:
          day, month, year = map(int, value.split('.'))
          if not 1 <= month <= 12 or not 1 <= day <= 31 or year < 1900:
                raise ValueError("Invalid date: day, month or year is out of range.")
          if month == 2:
            if day == 29 and not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
                raise ValueError("Invalid date: February can have 29 days only in leap years.")
          return datetime(year, month, day)
      except ValueError as e:
          raise ValueError(f"Invalid date: {e}")
  
  def get_value(self):
      return self.value.strftime(Birthday.__DATE_FORMAT)
      
  def __str__(self):
      return self.value.strftime(Birthday.__DATE_FORMAT)

  @classmethod
  def get_upcoming_birthdays(cls, users):
      today = datetime.today().date()
      delta = today + timedelta(days=7)

      upcoming_birthdays = []
      for name, record in users.items():
          if record.get_birthday():
              user_date = cls.check_date(record.birthday.value.strftime(cls.__DATE_FORMAT), today)
              
              if user_date > delta:
                  continue

              if user_date.weekday() == 5:  # Saturday
                  new_date = cls.date_to_string(user_date, 1)
                  upcoming_birthdays.append({"name": name, "congratulation_date": new_date})
              elif user_date.weekday() == 6:  # Sunday
                  new_date = cls.date_to_string(user_date, 2)
                  upcoming_birthdays.append({"name": name, "congratulation_date": new_date})
              else:
                  upcoming_birthdays.append({"name": name, "congratulation_date": user_date.strftime(cls.__DATE_FORMAT)})

      return upcoming_birthdays

  @classmethod
  def get_date(cls, date):
      return datetime.strptime(date, cls.__DATE_FORMAT).date()

  @classmethod
  def check_date(cls, user_date, today):
      date_frmt = cls.get_date(user_date)
      this_year_birthday = date_frmt.replace(year=today.year)
      if this_year_birthday < today:
          return this_year_birthday.replace(year=today.year + 1)
      else:
          return this_year_birthday

  @classmethod
  def date_to_string(cls, date, plus_day=0, format="%d.%m.%Y"):
      return (date + timedelta(days=plus_day)).strftime(format)