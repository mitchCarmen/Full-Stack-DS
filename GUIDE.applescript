



# MAY NEED TO INSTALL 'WTFORMS' IN DIGIOCEAN SERVER

python3 -m pip install wtforms





# IN DO SERVER TERMINAL, OPEN 8080 PORT

sudo ufw allow 8080





# IN DO SERVER TERMINAL, NAVIGATE TO THE DIR WITH 'start_server.sh' and run command 'sh start_server.sh' to start Flask

root@ubuntu-s-1vcpu-1gb-nyc1-01:~/Full-Stack-Mitchs/src# sh start_server.sh 

# Now flask app is running because we manually turned it on.
# To turn OFF, <CTRL> + <C>

# To PERMANENTLY run the Flask app, use the below:
root@ubuntu-s-1vcpu-1gb-nyc1-01:~/Full-Stack-Mitchs/src# nohup sh start_server.sh &

http://198.199.74.34:8080/



# USE THE BELOW IN A NEW LOCAL TERMINAL TO TEST

(base) mitchell.carmen@mcarmen-mb-Y70RJ:/$ curl -i -H 'Content-Type: application/json' -X POSt -d '[{"FlightDate":"2010-01-10","DepTime":"12:25","UniqueCarrier":"9E","Origin":"ATL","Dest":"AUS","Distance":"813.0"}]' http://198.199.74.34:8080/api/