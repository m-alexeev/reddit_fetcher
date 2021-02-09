from psaw import PushshiftAPI

api = PushshiftAPI()

gen = api.search_submissions(limit=100)
results = list(gen)
print (results)