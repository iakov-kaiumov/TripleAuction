import AuctionStep as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        yield Bid, dict(bid_a=cu(99), bid_b=cu(99), bid_c=cu(99))
        yield Results