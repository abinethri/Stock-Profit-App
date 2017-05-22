Stock Portfolio suggestion engine is hosted in 'pythonanywhere' cloud platform. 

The Stock Portfolio suggestion engine can also be hosted on a local server. 

Following sections provide instruction on how to access the suggestion engine in the cloud as well as steps to run the Stock Portfolio suggestion engine on a local server.

Please follow the below instructions to access stock suggestion engine hosted in the cloud.
1. Access http://abinethri.pythonanywhere.com/stocks/historyData ->  This will populate history in the sqlite database for all the 25 companies. This operation will take 5-8 mins to complete. After populating the database, you will see the response  "Finished populating the db with stock history." in the webpage.
2. Once the previous operation is successful, access http://abinethri.pythonanywhere.com/stocks/ to access the Stock suggestion engine home page
	

Please follow the below instructions to access stock suggestion engine to run it on a local server
Following instructions depends on python-2.7 being installed in the system
1. virtualenv myvenv -> This creates a virtual environment inside which the server will run
2. source myvenv/bin/activate
3. pip install django~=1.11.1
4. pip install requests
5. pip install googlefinance
6. pip install django_chartit
7. pip install yahoo_finance
8. rm -rf stockProfit/migrations/
9. rm -f db.sqlite3 
10. python manage.py makemigrations
11.  python manage.py migrate --run-syncdb
12. python manage.py runserver
13. Access http://127.0.0.1/stocks/historyData  via browser-> This will populate history in the sqlite database for all the 25 companies. This operation will take 5-8 mins to complete. After populating the database, you will see the response  "Finished populating the db with stock history." in the webpage.
14. Once the previous operation is successful, access http://127.0.0.1/stocks to access the Stock suggestion engine home page
