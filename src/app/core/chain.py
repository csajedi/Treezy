from Naked.toolshed.shell import muterun_js
from loguru import logger
class Chain:
    """abstraction to handle the chain calls to js and automatically make the result awaitable. Logging for the response object is also done here"""
    def __init__(self):
        """sets up the chain object, assumes py_anchor_root.js is found in the same directory. 
        Returns:
        True if the js file exited successfully, False otherwise """
        self.block = 0
    def anchor(self, root):
        response = muterun_js('../../chain/py_anchor_root.js',arguments=root)
        logger.info("Anchoring attempt {block} returned with {resp}" ,block=self.block, resp=response.stdout.)
        if response.exitcode == 0:
            self.block += 1
            return True
        else:
            return False

if __name__=='__main__':

    ch = Chain()
    resp = ch.anchor(root="000000000000000000000000000000000000")
    # pprint(resp)