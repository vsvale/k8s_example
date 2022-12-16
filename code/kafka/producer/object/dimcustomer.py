# import libraries
from random import randint,choice, uniform
from datetime import datetime
from faker import Faker
import pandas as pd
from faker.providers import DynamicProvider
import sqlite3
from deep_translator import GoogleTranslator


# Connect to the database
con = sqlite3.connect('courses_database') 

# Run SQL          
sql_query = pd.read_sql('SELECT distinct AddressID FROM sampledb.SalesLT.Address', con)

# Convert SQL to DataFrame
df = pd.DataFrame(sql_query, columns = ['AddressID'])
geographykeys = df['AddressID'].tolist()

con.close()

geographykeys_provider = DynamicProvider(
     provider_name="geography_keys",
     elements=geographykeys,
)

maritalstatus_provider = DynamicProvider(
     provider_name="marital_status",
     elements=["S","M","D","R","W"],
)

# set faker class
fake = Faker()
fake.add_provider(geographykeys_provider)
fake.add_provider(maritalstatus_provider)

# get seed
Faker.seed(randint(0, 123456789012345678901234567890))


# tester class
class Customers(object):

    # explicitly declare all schema members
    __slots__ = [
                    "customerkey",
                    "geographykey",
                    "customeralternatekey",
                    "title",
                    "firstname",
                    "middlename",
                    "lastname",
                    "namestyle",
                    "birthdate",
                    "maritalstatus",
                    "suffix",
                    "gender",
                    "emailaddress",
                    "yearlyincome",
                    "totalchildren",
                    "numberchildrenathome",
                    "englisheducation",
                    "spanisheducation",
                    "frencheducation",
                    "englishoccupation",
                    "spanishoccupation",
                    "frenchoccupation",
                    "houseownerflag",
                    "numbercarsowned",
                    "addressline1",
                    "addressline2",
                    "phone",
                    "datefirstpurchase",
                    "commutedistance"
                ]

    # define init 
    def __init__(self):

        self.customerkey = randint(1, 1234567890123456789012345678901)
        self.geographykey = fake.geographykeys_provider()
        self.customeralternatekey = "AW0"+str(self.customerkey)
        self.title = choice([fake.prefix(),None])
        self.firstname = fake.first_name()
        self.middlename = fake.random_uppercase_letter()
        self.lastname = fake.last_name()
        self.namestyle = 0
        self.birthdate = fake.date_of_birth()
        self.maritalstatus = fake.maritalstatus_provider()
        self.suffix = choice([fake.suffix(),None])
        self.gender = choice(["M","F"])
        self.emailaddress = fake.free_email()
        self.yearlyincome = round(uniform(15000.00,500000.00), 2)
        self.totalchildren = randint(1,3) * randint(0,1)
        self.numberchildrenathome = randint(0,self.totalchildren)
        self.englisheducation = choice(["Bachelors","Graduate Degree","High School","Partial College","Partial High School"])
        self.spanisheducation = GoogleTranslator(source='auto', target='spanish').translate(self.englisheducation)
        self.frencheducation = GoogleTranslator(source='auto', target='french').translate(self.englisheducation)
        self.englishoccupation = fake.job()
        self.spanishoccupation = GoogleTranslator(source='auto', target='spanish').translate(self.englishoccupation)
        self.frenchoccupation = GoogleTranslator(source='auto', target='french').translate(self.englishoccupation)
        self.houseownerflag = randint(0,1)
        self.numbercarsowned = randint(0,4)
        self.addressline1 = fake.address() 
        self.addressline2 = fake.country() 
        self.phone = fake.phone_number()
        self.datefirstpurchase = fake.date()
        self.commutedistance = choice(["0-1 Miles","1-2 Miles","2-5 Miles","5-10 Miles","10+ Miles"])


    # dict [output] = to_dict_rows
    def to_dict_rows(self):

        return {
                "customerkey":self.customerkey,
                "geographykey":self.geographykey,
                "customeralternatekey":self.customeralternatekey,
                "title":self.title,
                "firstname":self.firstname,
                "middlename":self.middlename,
                "lastname":self.lastname,
                "namestyle":self.namestyle,
                "birthdate":self.birthdate,
                "maritalstatus":self.maritalstatus,
                "suffix":self.suffix,
                "gender":self.gender,
                "emailaddress":self.emailaddress,
                "yearlyincome":self.yearlyincome,
                "totalchildren":self.totalchildren,
                "numberchildrenathome":self.numberchildrenathome,
                "englisheducation":self.englisheducation,
                "spanisheducation":self.spanisheducation,
                "frencheducation":self.frencheducation,
                "englishoccupation":self.englishoccupation,
                "spanishoccupation":self.spanishoccupation,
                "frenchoccupation":self.frenchoccupation,
                "houseownerflag":self.houseownerflag,
                "numbercarsowned":self.numbercarsowned,
                "addressline1":self.addressline1,
                "addressline2":self.addressline2,
                "phone":self.phone,
                "datefirstpurchase":self.datefirstpurchase,
                "commutedistance":self.commutedistance
        }

    # dict [output] = to_dict_events
    def to_dict_events(self):


        return {
                "customerkey":self.customerkey,
                "geographykey":self.geographykey,
                "customeralternatekey":self.customeralternatekey,
                "title":self.title,
                "firstname":self.firstname,
                "middlename":self.middlename,
                "lastname":self.lastname,
                "namestyle":self.namestyle,
                "birthdate":str(self.birthdate),
                "maritalstatus":self.maritalstatus,
                "suffix":self.suffix,
                "gender":self.gender,
                "emailaddress":self.emailaddress,
                "yearlyincome":self.yearlyincome,
                "totalchildren":self.totalchildren,
                "numberchildrenathome":self.numberchildrenathome,
                "englisheducation":self.englisheducation,
                "spanisheducation":self.spanisheducation,
                "frencheducation":self.frencheducation,
                "englishoccupation":self.englishoccupation,
                "spanishoccupation":self.spanishoccupation,
                "frenchoccupation":self.frenchoccupation,
                "houseownerflag":self.houseownerflag,
                "numbercarsowned":self.numbercarsowned,
                "addressline1":self.addressline1,
                "addressline2":self.addressline2,
                "phone":self.phone,
                "datefirstpurchase":str(self.datefirstpurchase),
                "commutedistance":self.commutedistance
        }

    # request multiple rows (events) at a time
    @staticmethod
    def get_multiple_rows(gen_dt_rows):

        # set init variables
        list_return_data = []
        for i in range(gen_dt_rows):
            customerkey = randint(1, 1234567890123456789012345678901)
            englisheducation = choice(["Bachelors","Graduate Degree","High School","Partial College","Partial High School"])
            englishoccupation = fake.job()
            children = randint(1,3) * randint(0,1)

            item =  {
                "customerkey":randint(1, 1234567890123456789012345678901),
                "geographykey":fake.geographykeys_provider(),
                "customeralternatekey":"AW0"+str(customerkey),
                "title":choice([fake.prefix(),None]),
                "firstname":fake.first_name(),
                "middlename":fake.random_uppercase_letter(),
                "lastname":fake.last_name(),
                "namestyle":0,
                "birthdate":fake.date_of_birth(),
                "maritalstatus":fake.maritalstatus_provider(),
                "suffix":choice([fake.suffix(),None]),
                "gender":choice(["M","F"]),
                "emailaddress":fake.free_email(),
                "yearlyincome":round(uniform(15000.00,500000.00), 2),
                "totalchildren":children,
                "numberchildrenathome":randint(0,children),
                "englisheducation":englisheducation,
                "spanisheducation":GoogleTranslator(source='auto', target='spanish').translate(englisheducation),
                "frencheducation":GoogleTranslator(source='auto', target='french').translate(englisheducation),
                "englishoccupation":englishoccupation,
                "spanishoccupation":GoogleTranslator(source='auto', target='spanish').translate(englishoccupation),
                "frenchoccupation":GoogleTranslator(source='auto', target='french').translate(englishoccupation),
                "houseownerflag":randint(0,1),
                "numbercarsowned":randint(0,4),
                "addressline1":fake.address(),
                "addressline2":fake.country(),
                "phone":fake.phone_number(),
                "datefirstpurchase":fake.date(),
                "commutedistance":choice(["0-1 Miles","1-2 Miles","2-5 Miles","5-10 Miles","10+ Miles"])
            }
        list_return_data.append(item)

        # convert list to pandas dataframe
        df_list_data = pd.DataFrame(list_return_data)
        return_dt = df_list_data.to_dict('records')
        return return_dt

    # log compaction demo
    @staticmethod
    def log_compaction(gen_dt_rows):

        # set init variables
        list_return_data = []
        for i in range(gen_dt_rows):
            customerkey = randint(1, 1234567890123456789012345678901)
            englisheducation = choice(["Bachelors","Graduate Degree","High School","Partial College","Partial High School"])
            englishoccupation = fake.job()
            children = randint(1,3) * randint(0,1)

            item =  {
                "customerkey":randint(1, 1234567890123456789012345678901),
                "geographykey":fake.geographykeys_provider(),
                "customeralternatekey":"AW0"+str(customerkey),
                "title":choice([fake.prefix(),None]),
                "firstname":fake.first_name(),
                "middlename":fake.random_uppercase_letter(),
                "lastname":fake.last_name(),
                "namestyle":0,
                "birthdate":str(fake.date_of_birth()),
                "maritalstatus":fake.maritalstatus_provider(),
                "suffix":choice([fake.suffix(),None]),
                "gender":choice(["M","F"]),
                "emailaddress":fake.free_email(),
                "yearlyincome":round(uniform(15000.00,500000.00), 2),
                "totalchildren":children,
                "numberchildrenathome":randint(0,children),
                "englisheducation":englisheducation,
                "spanisheducation":GoogleTranslator(source='auto', target='spanish').translate(englisheducation),
                "frencheducation":GoogleTranslator(source='auto', target='french').translate(englisheducation),
                "englishoccupation":englishoccupation,
                "spanishoccupation":GoogleTranslator(source='auto', target='spanish').translate(englishoccupation),
                "frenchoccupation":GoogleTranslator(source='auto', target='french').translate(englishoccupation),
                "houseownerflag":randint(0,1),
                "numbercarsowned":randint(0,4),
                "addressline1":fake.address(),
                "addressline2":fake.country(),
                "phone":fake.phone_number(),
                "datefirstpurchase":str(fake.date()),
                "commutedistance":choice(["0-1 Miles","1-2 Miles","2-5 Miles","5-10 Miles","10+ Miles"])
            }
        list_return_data.append(item)

        # convert list to pandas dataframe
        df_list_data = pd.DataFrame(list_return_data)
        return_dt = df_list_data.to_dict('records')
        return return_dt