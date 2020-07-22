import api

lower_div_cs_courses = api.fetch_courses("COM SCI", api.UPPER_DIV)

for course in lower_div_cs_courses:
    print(course)