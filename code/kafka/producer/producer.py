import settings
import delivery_reports
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from object.dimcustomer import Customers

class CustomerAvro(object):
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


    def __init__(self,customerkey=None,geographykey=None,customeralternatekey=None,title=None,firstname=None,middlename=None,lastname=None,namestyle=None,birthdate=None,maritalstatus=None,suffix=None,gender=None,emailaddress=None,yearlyincome=None,totalchildren=None,numberchildrenathome=None,englisheducation=None,spanisheducation=None,frencheducation=None,englishoccupation=None,spanishoccupation=None,frenchoccupation=None,houseownerflag=None,numbercarsowned=None,addressline1=None,addressline2=None,phone=None,datefirstpurchase=None,commutedistance=None):

        self.customerkey = customerkey
        self.geographykey = geographykey
        self.customeralternatekey = customeralternatekey
        self.title = title
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.namestyle = namestyle
        self.birthdate = birthdate
        self.maritalstatus = maritalstatus
        self.suffix = suffix
        self.gender = gender
        self.emailaddress = emailaddress
        self.yearlyincome = yearlyincome
        self.totalchildren = totalchildren
        self.numberchildrenathome = numberchildrenathome
        self.englisheducation = englisheducation
        self.spanisheducation = spanisheducation
        self.frencheducation = frencheducation
        self.englishoccupation = englishoccupation
        self.spanishoccupation = spanishoccupation
        self.frenchoccupation = frenchoccupation
        self.houseownerflag = houseownerflag
        self.numbercarsowned = numbercarsowned
        self.addressline1 = addressline1
        self.addressline2 = addressline2
        self.phone = phone
        self.datefirstpurchase = datefirstpurchase
        self.commutedistance = commutedistance

    # avro does not support code generation
    # need to provide dict representation
    def to_dict(self):

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

    @staticmethod
    def avro_producer(broker, schema_registry,schema_key, schema_value, kafka_topic,num_rows):

        # init producer using key & value [schema registry] integration
        producer = AvroProducer(
            settings.producer_settings_avro(broker,schema_registry),
            default_key_schema=avro.loads(schema_key),
            default_value_schema=avro.loads(schema_value)
        )

        # get data to insert
        get_data = Customers().get_multiple_rows(num_rows)

        inserts = 0
        while inserts < len(get_data):

            record = CustomerAvro()

            try:
                record.customerkey = get_data[inserts]['customerkey']
                record.geographykey = get_data[inserts]['geographykey']
                record.customeralternatekey = get_data[inserts]['customeralternatekey']
                record.title = get_data[inserts]['title']
                record.firstname = get_data[inserts]['firstname']
                record.middlename = get_data[inserts]['middlename']
                record.lastname = get_data[inserts]['lastname']
                record.namestyle = get_data[inserts]['namestyle']
                record.birthdate = get_data[inserts]['birthdate']
                record.maritalstatus = get_data[inserts]['maritalstatus']
                record.suffix = get_data[inserts]['suffix']
                record.gender = get_data[inserts]['gender']
                record.emailaddress = get_data[inserts]['emailaddress']
                record.yearlyincome = get_data[inserts]['yearlyincome']
                record.totalchildren = get_data[inserts]['totalchildren']
                record.numberchildrenathome = get_data[inserts]['numberchildrenathome']
                record.englisheducation = get_data[inserts]['englisheducation']
                record.spanisheducation = get_data[inserts]['spanisheducation']
                record.frencheducation = get_data[inserts]['frencheducation']
                record.englishoccupation = get_data[inserts]['englishoccupation']
                record.spanishoccupation = get_data[inserts]['spanishoccupation']
                record.frenchoccupation = get_data[inserts]['frenchoccupation']
                record.houseownerflag = get_data[inserts]['houseownerflag']
                record.numbercarsowned = get_data[inserts]['numbercarsowned']
                record.addressline1 = get_data[inserts]['addressline1']
                record.addressline2 = get_data[inserts]['addressline2']
                record.phone = get_data[inserts]['phone']
                record.datefirstpurchase = get_data[inserts]['datefirstpurchase']
                record.commutedistance = get_data[inserts]['commutedistance']

                # server on_delivery callbacks from previous asynchronous produce()
                producer.poll(0)

                # message passed to the delivery callback will already be serialized.
                # to aid in debugging we provide the original object to the delivery callback.
                producer.produce(
                    topic=kafka_topic,
                    key={'customerkey': record.customerkey},
                    value=record.to_dict(),
                    callback=lambda err, msg, obj=record: delivery_reports.on_delivery_avro(err, msg, obj)
                )

            except BufferError:
                print("buffer full")
                producer.poll(0.1)

            except ValueError:
                print("invalid input")
                raise

            except KeyboardInterrupt:
                raise

            # increment values
            inserts += 1

        print("flushing records...")

        # buffer messages to send
        producer.flush()