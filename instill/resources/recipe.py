# pylint: disable=no-member,wrong-import-position
import instill.protogen.vdp.pipeline.v1beta.pipeline_pb2 as pipeline_pb


def create_recipe(component: list) -> pipeline_pb.Recipe:
    recipe = pipeline_pb.Recipe()
    recipe.version = "v1beta"
    recipe.components.extend(component)

    return recipe
