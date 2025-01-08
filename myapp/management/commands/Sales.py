from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from myapp.models import CustomerData


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from CustomerData.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if CustomerData.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading childrens data")


        #Code to load the data into database
        for row in DictReader(open('./CustomerData.csv')):
            child=CustomerData(user_id=row['User_ID'], cust_name=row['Cust_name'], product_id=row['Product_ID'],gender=row['Gender'],age_group=row["Age Group"],age=row["Age"],marital_status=row["Marital_Status"],state=row["State"],zone=row["Zone"],occupation=row["Occupation"],product_category=row["Product_Category"],orders=row["Orders"],amount=row["Amount"])  
            child.save()
				 			
