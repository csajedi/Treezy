from time import sleep
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
        response = muterun_js('../../chain/py_anchor_root.js',root)
        # sleep(60)
        logger.info("Anchoring attempt {block} returned with {resp}" ,block=self.block, resp=response.stdout)
        
        if response.exitcode == 0:
            logger.info("Anchoring attempt {block} success" ,block=self.block)
            self.block += 1
            # the command was successful, handle the standard output
            standard_out = response.stdout
            print(standard_out)
            return True
        else:
            # the command failed or the executable was not present, handle the standard error
            standard_err = str(response.stderr)
            exit_code = str(response.exitcode)
            print('Exit Status ' + exit_code + ': ' + standard_err)
            logger.info("Anchoring attempt {block} failed" ,block=self.block)
            return False

if __name__=='__main__':

    ch = Chain()
    resp = ch.anchor(root="000000000000000000000000000000000000")
    # pprint(resp)