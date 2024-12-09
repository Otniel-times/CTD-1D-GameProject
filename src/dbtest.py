import dbHandler

#dbHandler.new_entry("hello3", 150)
data = dbHandler.getall_username_and_score_sorted()
print(data)

everything = dbHandler.get_all()
print(everything)