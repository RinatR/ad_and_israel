import json 

# from flaskblog.models import City
# from flaskblog import db

# with open('posts.json') as f: 
# 	data = json.load(f) 
# 	for post in data: 
# 		user = User.query.get(post['user_id']) 
# 		if user: 
# 			post = Post(title=post['title'], content=post['content'], user_id=post['user_id']) 
# 			db.session.add(post) 
# 			db.session.commit()

with open('cities.json') as f: 
	data = json.load(f) 
	city_list = []
	for city in data: 	
		if city['country'] == "RU":
			city_list.append(city['name'])
		# city = City(name=city['city'].lower(), region=city['region'].lower(), country_id=1) 
		# db.session.add(city) 
		# db.session.commit()
	city_list.sort()
	print(city_list)