import tweepy as tp
import csv
import time

access_token = "801652357549277184-5Vwi8gky57Eq3bXUMJ1zG8ZDNFIgmmX"
access_token_secret = "kxjbCgdauTqlyUwqlnxwdDltC2XzN7ucbV43nG7tdP6GF"
api_key = "uxpyqQjhlBpv96WLJHMrtUjb0"
api_secret = "62DBVhEeiI9EqaZOLlEY8vt7HuC5V5wu4mbKjmKjykxKa26HoM"
file="/home/daanish/Desktop/Project/MachineLearning/Twitter/files/tweetscyclone.csv"
hashtag="#CyclonePhethai"
# hashtag="#Phethai"
maxitems=999999999	
row=["SNo","Time","Location","Text"]

class Read:
	
	def __init__(self):
		self.auth=tp.OAuthHandler(api_key,api_secret)
		self.auth.set_access_token(access_token,access_token_secret)
		self.api=tp.API(self.auth)
		return

	def append_to_csv(self,row):
		with open(file,'a') as cf:
			writer=csv.writer(cf)
			writer.writerow(row)
		cf.close()
		return

	def get_last_row(self):
		with open(file,'r') as cf:
			row=list(csv.reader(cf))
		if(len(row)==0):
			return []
		else:
			# return row[-1]
			return row[1]
			# return []

	def get_tweets(self):
		
		row=self.get_last_row()
		if(len(row)==0):
			self.append_to_csv(row)
			query=hashtag
		else:
			# query=hashtag+" until:{0}".format(row[1])
			query=hashtag+" since:{0}".format(row[1])
			# query=hashtag;
			print(query)

		cnt=0
		tweets=tp.Cursor(self.api.search,tweet_mode="extended",q=query).items(maxitems)
		while True:
			try:
				for tweet in tweets:
					cnt+=1
					self.append_to_csv([cnt,tweet.created_at,tweet.user.location.encode("utf-8"),tweet.full_text.encode("utf-8")])
			except tp.TweepError:
				print("SleepTime")
				time.sleep(60*15)
				print("WakeUpSid")
				continue
			except StopIteration:
				break
		return

r=Read()
r.get_tweets()



