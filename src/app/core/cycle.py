import asyncio


class Cycle:
    """ This singleton handles the waiting and firing of events to tightly-integrate the calendar to the Zilliqa block minting process.

    It assumes:

    - The ZILLIQA_NETWORK env variable is set.
    - The RPC is up, addressable.
    - The Account set in ZILLIQA_PKEY env variable has sufficient funds.
    """

    def __init__(self, interval=120):
        """sets up the async event loop
        Parameters:
        interval - the optional parameter for setting the time interval of the anchor.

        Returns: an object that tracks the current phase, spawns subtasks
        """
        self.phase = "collecting"  # collecting or sending
