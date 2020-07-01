"""The reactor singleton handles the contract interactions and overall state for the server, it is meant to be run in its own thread and fed time interval parameters for periodic anchoring, which it manages internally.
Possible states: - OpenSubmission, AnchorPending, AnchoredHash['hash'], 
"""
import threading
import time

from loguru import logger
from timeloop import Timeloop
from datetime import timedelta, datetime

from chain import Chain
from tree import Tree

class Reactor:
    """ Handles the waiting and firing of events to periodically anchor the the root hash.

    Assumes:
    - The chain/py_anchor_root.js file has all the correct variables defined
    """

    def __init__(self, tree, interval=60):
        """sets up the async event loop
        Parameters:
        tree - the same merkle tree instance being anchored
        interval - the optional parameter for setting the time interval of the anchor.

        Returns: an object that tracks the current phase, spawns subtasks
        """
        self.tree = tree
        self.loop = Timeloop()
        self.chain = Chain()
        self.interval = interval
        logger.info("The reactor was started at time: {time}", time=datetime.timestamp(datetime.now()))

    def start(self):

        # Kick off the anchoring event every 30 seconds
        @self.loop.job(interval=timedelta(seconds=self.interval))
        def anchor_tree():
            root = self.tree.get_current_root().decode('utf-8')
            self.chain.anchor(root)
            logger.info("anchored root: {} \t at  time: {} \t block: {}", root, datetime.timestamp(datetime.now()), self.chain.block)

        self.loop.start(block=True)

    def stop(self):
        """always ensure the loop has been manually stopped"""
        logger.info("timeloop stopping at time: {} \t block:{}", datetime.timestamp(datetime.now()), self.chain.block)
        self.loop.stop()
        

if __name__=='__main__':
    tree = Tree()
    rr = Reactor(tree, interval=10)
    while True:
        rr.start()