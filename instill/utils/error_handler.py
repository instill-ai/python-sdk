# pylint: disable=inconsistent-return-statements,no-member
import os

import grpc

from instill.utils.logger import Logger


class NotServingException(Exception):
    def __str__(self) -> str:
        return "target host is not serving"


def grpc_handler(func):
    def func_wrapper(*args, **kwargs):
        try:
            if not args[0].is_serving():
                raise NotServingException
            return func(*args, **kwargs)
        except grpc.RpcError as rpc_error:
            Logger.w(rpc_error.code())
            Logger.w(rpc_error.details())
        except Exception as e:
            Logger.exception(e)
            os._exit(1)

    return func_wrapper
