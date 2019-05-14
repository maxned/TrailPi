from werkzeug.routing import BaseConverter
from datetime import datetime

class ListConverter(BaseConverter):
  def to_python(self, value):
    return value.split('+')
  
  def to_url(self, values):
    return '+'.join(BaseConverter.to_url(value)
                    for value in values)

def get_local_date():
  local_date = datetime.now()
  return local_date.strftime('%Y-%m-%d')