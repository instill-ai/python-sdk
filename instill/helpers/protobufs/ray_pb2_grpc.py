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
        self.Trigger = channel.unary_unary(
                '/ray.v1.RayService/Trigger',
                request_serializer=ray__pb2.TriggerRequest.SerializeToString,
                response_deserializer=ray__pb2.TriggerResponse.FromString,
                )


class RayServiceServicer(object):
    """Ray service for internal process
    """

    def Trigger(self, request, context):
        """Trigger method is the defaut trigger entry for ray deployment
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RayServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Trigger': grpc.unary_unary_rpc_method_handler(
                    servicer.Trigger,
                    request_deserializer=ray__pb2.TriggerRequest.FromString,
                    response_serializer=ray__pb2.TriggerResponse.SerializeToString,
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
    def Trigger(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ray.v1.RayService/Trigger',
            ray__pb2.TriggerRequest.SerializeToString,
            ray__pb2.TriggerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
