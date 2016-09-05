from peewee import *
from passlib.apps import postgres_context

psql_db = PostgresqlDatabase(
    'postgres',
    user='prabhath',
    password='',
    host='localhost',
)


class BaseModel(Model):

    class Meta:
        database = psql_db
        db_table = 'city'
        table_alias = 'c'


class City(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=35)
    countrycode = CharField(max_length=3)
    district = CharField(max_length=20)
    population = BigIntegerField()

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'name': str(self.name).strip(),
            'countrycode': str(self.countrycode).strip(),
            'district': str(self.district).strip(),
            'population': self.population,
        }

        return data

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(
            self.id,
            self.name,
            self.countrycode,
            self.district,
            self.population
        )

class UserData(Model):
    id = PrimaryKeyField(null=False)
    username = CharField(max_length=50, unique=True)
    password_hash = CharField(max_length=128)

    @property
    def serialize(self):
        data = {
        'id': self.id,
        'username': self.username,
        'password_hash': self.password_hash
        }

        return data

    def __repr__(self):
        return "id: {id} - name: {name}" .format(id=self.id, name=self.username)

    def hash_password(self):
        self.password_hash = postgres_context.encrypt(self.password_hash, user="prabhath")

    def verify_password(self, password):
        return postgres_context.verify(password, self.password_hash , user="prabhath")

    class Meta:
        database = psql_db
