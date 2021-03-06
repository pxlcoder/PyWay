import PyWay

p = PyWay.createInterface()

# Get full schedule for a route at a specific stop
print p.getFullSchedule(1306,26,"West")

# Get next three passing times for a route at a specific stop
print p.getNextPassingTime(1306,26,"West")

# Get all stop names and numbers for a route
print p.getRouteStops(26,"West")

# Access previously loaded schedules
print p.cachedSchedules[p.createID(1306,26,"West")]

# Access name and number of previously loaded stops
print p.cachedStops["1306"]
