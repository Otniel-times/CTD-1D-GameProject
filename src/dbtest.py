import dbHandler

print(dbHandler.new_entry("hello",1, 100))
data = dbHandler.getall_username_and_score_sorted()
print(data)
