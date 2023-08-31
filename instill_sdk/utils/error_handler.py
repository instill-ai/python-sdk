# pylint: disable=inconsistent-return-statements
import os

import grpc

from instill_sdk.utils.logger import Logger


def grpc_handler(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except grpc.RpcError as rpc_error:
            Logger.exception(rpc_error)
        except Exception as e:
            Logger.exception(e)
            os._exit(1)

    return func_wrapper
