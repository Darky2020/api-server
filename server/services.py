from .models import Transaction
from .models import Address
from .models import Balance
from .models import Output
from .models import Input
from .models import Block
from pony import orm

class BlockService(object):
    @classmethod
    def latest_block(cls):
        return Block.select().order_by(
            orm.desc(Block.height)
        ).first()

    @classmethod
    def create(cls, reward, blockhash, height, created,
               difficulty, merkleroot, chainwork, version,
               weight, stake, nonce, size, bits,
               signature=None):
        return Block(
            reward=reward, blockhash=blockhash, height=height, created=created,
            difficulty=difficulty, merkleroot=merkleroot, chainwork=chainwork, version=version,
            weight=weight, stake=stake, nonce=nonce, size=size, bits=bits,
            signature=signature
        )

    @classmethod
    def get_by_hash(cls, bhash):
        return Block.get(blockhash=bhash)

    @classmethod
    def get_by_height(cls, height):
        return Block.get(height=height)

    @classmethod
    def blocks(cls, page=1, pagesize=100):
        return Block.select().order_by(
            orm.desc(Block.height)
        ).page(page, pagesize=pagesize)

    @classmethod
    def chart(cls):
        query = orm.select((b.height, len(b.transactions)) for b in Block)
        query = query.order_by(-1)
        return query[:1440]

class TransactionService(object):
    @classmethod
    def get_by_txid(cls, txid):
        return Transaction.get(txid=txid)

    @classmethod
    def create(cls, amount, txid, created, locktime, size, block,
               coinbase=False, coinstake=False):
        return Transaction(
            amount=amount, txid=txid, created=created,
            locktime=locktime, size=size, coinbase=coinbase,
            coinstake=coinstake, block=block
        )

    @classmethod
    def transactions(cls, page=1, pagesize=100):
        query = orm.select((o.transaction, sum(o.amount), o.transaction.id) for o in Output).distinct()
        query = query.order_by(-3)
        return query.page(page, pagesize=pagesize)

    @classmethod
    def total_transactions(cls):
        query = orm.select((orm.count(o.transaction)) for o in Output).distinct()
        return query.first()

    @classmethod
    def count(cls, rewards=False):
        return Transaction.select().count(distinct=False)

class InputService(object):
    @classmethod
    def create(cls, sequence, n, transaction, vout):
        return Input(
            sequence=sequence, transaction=transaction,
            vout=vout, n=n,
        )

class AddressService(object):
    @classmethod
    def get_by_address(cls, address):
        return Address.get(address=address)

    @classmethod
    def richlist(cls, page):
        query = orm.select(
            (b.address, b.amount) for b in Balance
        )

        query = query.order_by(-2)

        return query.page(page, pagesize=100)

    @classmethod
    def create(cls, address):
        return Address(address=address)

class BalanceService(object):
    @classmethod
    def get(cls, address):
        return Balance.get(
            address=address
        )

    @classmethod
    def create(cls, address):
        return Balance(
            address=address
        )

class OutputService(object):
    @classmethod
    def get_by_prev(cls, transaction, n):
        return Output.get(transaction=transaction, n=n)

    @classmethod
    def create(cls, transaction, amount, category, address, raw, n):
        return Output(
            transaction=transaction, amount=amount, category=category,
            address=address, raw=raw, n=n
        )