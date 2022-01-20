import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler




event1 = datetime.datetime(year=1920,
   month=12, day=24)
event2 = datetime.datetime.now()
agewine = event2 - event1

event1_year = event1.year
event2_year= event2.year
agewine_year = event2_year-event1_year

print(agewine_year)



server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

