import time

class Transaction:
  def __init__(self, sender, receiver, coins):
    self.sender = sender
    self.receiver = receiver
    self.timestamp = time.time()
    self.coins = coins