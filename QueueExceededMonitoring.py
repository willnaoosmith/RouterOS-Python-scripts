#!/usr/bin/python

import routeros_api


connection = routeros_api.RouterOsApiPool(
    "host",
    username="username",
    password="password",
    port=port,
	plaintext_login=True
)

api = connection.get_api()

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

ExceededQueues = [
	queue for queue in Fetchedresults
	if (queue["usageUpload"] > queue["LimitUpload"] and queue["LimitUpload"] != 0 ) or (queue["usageDownload"] > queue["LimitDownload"] and queue["LimitDownload"] != 0)
]

print(ExceededQueues)
