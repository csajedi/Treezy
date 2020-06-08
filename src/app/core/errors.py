# errors
import fastapi_jsonrpc as jsonrpc


class ChecksumFormatError(jsonrpc.BaseError):
    CODE = 6000
    MESSAGE = "Checksum improperly formed error"


class ValidationError(jsonrpc.BaseError):
    CODE = 6001
    MESSAGE = "The proof could not be validated"


class ChecksumNotFoundError(jsonrpc.BaseError):
    CODE = 6002
    MESSAGE = "Checksum is not in the merkle tree"


class ChecksumExistsError(jsonrpc.BaseError):
    CODE = 6003
    MESSAGE = "Checksum is already in the merkle tree"
