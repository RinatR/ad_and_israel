import json 

from flaskblog.models import Region, Country
from flaskblog import db


# with open('posts.json') as f: 
# 	data = json.load(f) 
# 	for post in data: 
# 		user = User.query.get(post['user_id']) 
# 		if user: 
# 			post = Post(title=post['title'], content=post['content'], user_id=post['user_id']) 
# 			db.session.add(post) 
# 			db.session.commit()

with open('russia.json') as f: 
	data = json.load(f) 
	regions_list = []
	for r in data:
		regions_list.append(r['region'])

	unq_regions = set(regions_list)
	
	sorted_regions = sorted(unq_regions)
	for r in sorted_regions:
		# print(r)		
			region = Region(name=r.lower()) 
			db.session.add(region) 
			db.session.commit()

# regions = Region.query.all()
# print(regions)




