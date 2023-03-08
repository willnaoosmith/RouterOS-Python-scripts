#!/usr/bin/python

from time import sleep
import routeros_api

ExceededQueuesList = []

FrequencyInSeconds = 1
Limit = 5

connection = routeros_api.RouterOsApiPool(
    "host",
    username="username",
    password="password",
    port=port,
	plaintext_login=True
)


api = connection.get_api()

def getQueues():
	list_queues = api.get_resource("/queue/simple")

	Fetchedresults = [
		{
			"name": queue["name"],
			"LimitUpload": int(queue["limit-at"].split("/")[0]),
			"LimitDownload": int(queue["limit-at"].split("/")[1]),
			"usageUpload": int(queue["rate"].split("/")[0]),
			"usageDownload": int(queue["rate"].split("/")[1])
		}
		for queue in list_queues.get()
	]

	for queue in Fetchedresults:
		if (queue["usageUpload"] > queue["LimitUpload"] and queue["LimitUpload"] != 0 ) or (queue["usageDownload"] > queue["LimitDownload"] and queue["LimitDownload"] != 0):
			CheckQueue = next((exceededQueue for exceededQueue in ExceededQueuesList if exceededQueue['name'] == queue['name']), None)

			if(CheckQueue['count'] == limit):
				print("Limit Exceeded, send alert")

			if not CheckQueue:
				ExceededQueuesList.append({
					"name": queue['name'],
					"count": 0
				})

			else:
				if CheckQueue['count'] <= limit:
					CheckQueue['count'] += 1

	for queue in ExceededQueuesList:
		CheckQueue = next((newQueue for newQueue in Fetchedresults if newQueue['name'] == queue['name']), None)

		if not CheckQueue:
			ExceededQueuesList.remove(CheckQueue)

while True:
	getQueues()
	print(ExceededQueuesList)
	sleep(FrequencyInSeconds)