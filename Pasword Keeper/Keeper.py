from hashlib import sha256

def get_hexdigest(salt, plaintext):
    return sha256(salt.encode('utf-8') + plaintext.encode('utf-8')).hexdigest()

SECRET_KEY = 's3cr3t'

def make_password(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, service)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return ''.join((salt, hsh))
ALPHABET = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@#$%^&*()-_')
def password(plaintext, service, length=10):
    raw_hexdigest = make_password(plaintext, service)
    num = int(raw_hexdigest, 16)
    num_chars = len(ALPHABET)
    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(ALPHABET[idx])

    return ''.join(chars)

from peewee import *

db = SqliteDatabase('accounts.db')

class Service(Model):
    name = CharField()
    length = IntegerField(default=8)
    pwd = CharField()
    symbols = BooleanField(default=True)
    alphabet = CharField(default='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    class Meta:
        database = db

    def get_alphabet(self):
        if self.alphabet:
            return self.alphabet
        alpha = ('abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                 '0123456789')
        if self.symbols:
            alpha += '!@#$%^&*()-_'
        return alpha

    def password(self, plaintext):
        return password(plaintext, self.name, self.length)

    @classmethod
    def search(cls, q):
        return cls.select().where(cls.name ** ('%%%s%%' % q))

db.create_table(Service, True)
#################################################################
#                   Crear constraseñas                          #
#################################################################
#primero defino los servicios (o paginas web) en los que quiero usar este manager
#para este ejemplo pondre 2, uno que permita usar simbolos y otro que no
Facebook= Service.create(name='Facebook', length=8, symbols=True, pwd=password('carlosFacebook', 'Facebook', 8))
Twitter= Service.create(name='Twitter', length=10, symbols=False, pwd=password('carlosTwitter', 'Twitter', 10))
#luego a cada una les defino un password base que es el que sera usado en el hashing.
Facebook.password('carlosFacebook')
Twitter.password('carlosTwitter')