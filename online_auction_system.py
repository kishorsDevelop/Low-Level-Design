"""
Requirements:-
---------------
1. Users should be able to register as bidders in the online auction system.
2. Each bidder should have a unique name.
3. Bidders should be able to place bids on items up for auction.
4. Bidders can place bids multiple times during the auction duration.
5. The system should notify bidders of ongoing auctions.
6. Bidders should receive notifications when other bidders place bids.
7. At the end of the auction, the system should determine and declare the winner.
8. The winner is the bidder with the highest bid amount.
9. The system should notify the winning bidder once the auction concludes.
10.Bidders should be able to interact with the system, placing bids and receiving notifications.

Actors:
---------
1. Bidders/Users
2. AuctionMediator

Entities/Classes:
-----------------
1. Bidder
2. AuctionMediator
3. OnlineAuctionMediators

"""
from abc import ABC, abstractmethod
class AuctionMediator(ABC):
    @abstractmethod
    def register_bidder(self, bidder):
        pass

    @abstractmethod
    def place_bid(self, bidder, bid_amount):
        pass
    
    @abstractmethod
    def notify_winner(self, winner):
        pass

class Bidder:
    def __init__(self, name, mediator):
        self.name = name
        self.mediator = mediator
        self.amount = 0
    
    def place_bid(self, bid_amount):
        self.amount = bid_amount
        self.mediator.place_bid(self, bid_amount)
    
    def notify(self, msg):
        print(f"{self.name} received notification: {msg} ")

    def notify_win(self):
        self.notify("You have won Auction.")

    def notify_lose(self):
        self.notify("You have lost auction.")

class OnlineAuctionMediator(AuctionMediator):
    def __init__(self):
        self.bidders = []

    def register_bidder(self, bidder):
        self.bidders.append(bidder)
    
    def place_bid(self, bidder, bid_amount):
        for other_bidder in self.bidders:
            if other_bidder != bidder:
                other_bidder.notify(f"{bidder.name} placed a bid of amount Rs.{bid_amount}")
    
    def notify_winner(self, winner):
        for bidder in self.bidders:
            if bidder.name == winner.name:
                bidder.notify_win()
            else:
                bidder.notify_lose()

if __name__ == '__main__':
    mediator = OnlineAuctionMediator()
    
    bidder1 = Bidder("Neeta Birla", mediator)
    bidder2 = Bidder("Mukesh Godrej", mediator)
    bidder3 = Bidder("Ratan Airtel", mediator)

    mediator.register_bidder(bidder1)
    mediator.register_bidder(bidder2)
    mediator.register_bidder(bidder3)

    bidder1.place_bid(100000000000)
    bidder2.place_bid(200000000000)
    bidder3.place_bid(300000000000)

    winner = max([bidder1, bidder2, bidder3], key=lambda bidder:bidder.amount)
    mediator.notify_winner(winner)
