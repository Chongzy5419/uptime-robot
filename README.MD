this is an uptime robot bot script to monitor the domain carrot.student.fsktm.um.edu.my using telegram bot API

a notification will be sent to the telegram user at user id 1021282117 using the telegram bot "uptime robot" if the domain is down

this program will run a curl to the destination domain at an interval of 60 second. If the returned http status code is not "200" , the script will call the function to send the telegram notification to the user

if a status down is recorded, the notification function will sleep for one hour before sending another notification to prevent spamming and reaching limit of the telegram API

