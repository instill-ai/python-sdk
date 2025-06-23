# pylint: disable=inconsistent-return-statements,no-member
import os

import grpc

from instill.utils.logger import Logger


class NotServingException(Exception):
    def __init__(self, message: str = "target host is not serving"):
        self.message = message

    def __str__(self) -> str:
        return self.message


class NamespaceException(Exception):
    def __init__(self, message: str = "namespace ID not available"):
        self.message = message

    def __str__(self) -> str:
        return self.message


def grpc_handler(func):
    def func_wrapper(*args, **kwargs):
        silent = kwargs.pop("silent", False)
        try:
            if not args[0].is_serving():
                raise NotServingException
            return func(*args, **kwargs)
        except grpc.RpcError as rpc_error:
            if not silent:
                Logger.w(rpc_error.code())
                Logger.w(rpc_error.details())
                os._exit(1)
        except Exception as e:
            Logger.exception(e)
            os._exit(1)

    return func_wrapper
