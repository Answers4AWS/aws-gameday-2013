#!/bin/python

import boto.sqs as sqs
import uuid

conn = sqs.connect_to_region("us-east-1")
queue = conn.get_queue("AwesomeInputQueue")

msgId = 0

urls = """http://upload.wikimedia.org/wikipedia/en/4/45/IRT_Composite_Interior.jpg
	http://upload.wikimedia.org/wikipedia/en/f/f2/R62A_SMS_2406_New_Seats_And_Flooring.JPG
 	http://upload.wikimedia.org/wikipedia/en/thumb/1/16/Train_of_Many_Colors.jpg/800px-Train_of_Many_Colors.jpg"""

#print(conn.send_message(queue, urls))
def createBatch(numMsgs):
	msgList = []
	for i in range(numMsgs):
		msgList.append([ str(i) + "-" + str(uuid.uuid4()), urls , 0])
	return msgList

msgs = createBatch(10)

for i in range(100000):
	batchResults = queue.write_batch(msgs)
	if(len(batchResults.errors) > 0):
		print("Batch %d had an error! Listing errors:"%  i)
		for err in batchResults.errors:
			print("id: %s\nsender_fault:%s\nerror_code:%s\nerror_message:%s" % (err.id, err.sender_fault, err.error_code, err.error_message))
	else:
		print("Batch %d Submitted Successfully." % i)

