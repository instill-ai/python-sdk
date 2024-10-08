# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import ray_pb2 as ray__pb2


class RayServiceStub(object):
    """Ray service for internal process
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.__call__ = channel.unary_unary(
                '/ray.v1.RayService/__call__',
                request_serializer=ray__pb2.CallRequest.SerializeToString,
                response_deserializer=ray__pb2.CallResponse.FromString,
                )


class RayServiceServicer(object):
    """Ray service for internal process
    """

    def __call__(self, request, context):
        """Trigger method is the defaut trigger entry for ray deployment
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RayServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            '__call__': grpc.unary_unary_rpc_method_handler(
                    servicer.__call__,
                    request_deserializer=ray__pb2.CallRequest.FromString,
                    response_serializer=ray__pb2.CallResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ray.v1.RayService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RayService(object):
    """Ray service for internal process
    """

    @staticmethod
    def __call__(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ray.v1.RayService/__call__',
            ray__pb2.CallRequest.SerializeToString,
            ray__pb2.CallResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
