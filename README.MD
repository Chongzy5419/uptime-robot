this is an uptime robot bot script to monitor the domain carrot.student.fsktm.um.edu.my using telegram bot API

a notification will be sent to the telegram user using the telegram bot "uptime robot" if the domain is down

this program will run a curl to the destination domain at an interval of 20 second. If the returned http status code is not "200" , the script will call the function to send the telegram notification to the user

if a status down is recorded, the notification function will sleep for 20 minutes before sending another notification to prevent spamming and reaching limit of the telegram API

if a domain was recorded to be down in previous attempt, a telegram message will be send via the telegram bot once the domain is restored
