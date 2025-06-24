"""Unit tests for resources."""

# pylint: disable=unused-argument,unused-variable,no-name-in-module,abstract-class-instantiated

from unittest.mock import Mock, patch

import grpc
import pytest
from google.longrunning.operations_pb2 import Operation
from google.protobuf.field_mask_pb2 import FieldMask
from google.protobuf.struct_pb2 import Struct

from instill.clients import InstillClient
from instill.resources.model import Model
from instill.resources.pipeline import Pipeline
from instill.resources.resource import Resource


def describe_resource():
    """Test the base Resource abstract class."""

    def test_resource_is_abstract():
        """Test that Resource is an abstract base class."""
        with pytest.raises(TypeError):
            Resource()  # type: ignore

    def test_resource_abstract_methods():
        """Test that Resource has required abstract methods."""

        # Create a concrete implementation for testing
        class ConcreteResource(Resource):
            def __init__(self):
                self._client = None
                self._resource = None

            @property
            def client(self):
                return self._client

            @client.setter
            def client(self, value):
                self._client = value

            @property
            def resource(self):
                return self._resource

            @resource.setter
            def resource(self, value):
                self._resource = value

        # Should not raise an error
        resource = ConcreteResource()
        assert resource is not None


def describe_model():
    """Test the Model resource class."""

    @pytest.fixture
    def mock_client():
        """Create a mock InstillClient."""
        client = Mock(spec=InstillClient)
        client.model = Mock()
        return client

    @pytest.fixture
    def mock_model_response():
        """Create a mock model response."""
        model = Mock()
        model.id = "test-model-id"
        model.model_definition = Mock()
        return model

    def test_model_initialization_existing_model(mock_client, mock_model_response):
        """Test Model initialization when model already exists."""
        # Setup
        mock_client.model.get_model.return_value = Mock(model=mock_model_response)

        # Execute
        model = Model(
            client=mock_client,
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )

        # Assert
        assert model.client == mock_client
        assert model.resource == mock_model_response
        mock_client.model.get_model.assert_called_once_with(
            model_name="test-model", silent=True
        )
        mock_client.model.create_model.assert_not_called()

    def test_model_initialization_new_model(mock_client, mock_model_response):
        """Test Model initialization when creating new model."""
        # Setup
        mock_client.model.get_model.return_value = None
        mock_client.model.create_model.return_value = Mock(model=mock_model_response)

        # Execute
        model = Model(
            client=mock_client,
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )

        # Assert
        assert model.client == mock_client
        assert model.resource == mock_model_response
        mock_client.model.get_model.assert_called_once_with(
            model_name="test-model", silent=True
        )
        mock_client.model.create_model.assert_called_once_with(
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )

    def test_model_initialization_creation_failed(mock_client):
        """Test Model initialization when model creation fails."""
        # Setup
        mock_client.model.get_model.return_value = None
        mock_client.model.create_model.return_value = Mock(model=None)

        # Execute & Assert
        with pytest.raises(BaseException, match="model creation failed"):
            Model(
                client=mock_client,
                name="test-model",
                definition="test-definition",
                configuration={"key": "value"},
            )

    def test_model_call_success(mock_client, mock_model_response):
        """Test Model __call__ method with successful response."""
        # Setup
        mock_client.model.get_model.return_value = Mock(model=mock_model_response)
        mock_response = Mock()
        mock_response.task_outputs = ["output1", "output2"]
        mock_client.model.trigger.return_value = mock_response

        model = Model(
            client=mock_client,
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )

        # Execute
        result = model(task_inputs=["input1"], silent=False)

        # Assert
        assert result == ["output1", "output2"]
        mock_client.model.trigger.assert_called_once_with(
            "test-model-id", ["input1"], silent=False
        )

    def test_model_call_no_response(mock_client, mock_model_response):
        """Test Model __call__ method with no response."""
        # Setup
        mock_client.model.get_model.return_value = Mock(model=mock_model_response)
        mock_client.model.trigger.return_value = None

        model = Model(
            client=mock_client,
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )

        # Execute
        result = model(task_inputs=["input1"], silent=True)

        # Assert
        assert result is None
        mock_client.model.trigger.assert_called_once_with(
            "test-model-id", ["input1"], silent=True
        )

    def test_model_properties(mock_client, mock_model_response):
        """Test Model property getters and setters."""
        # Setup
        mock_client.model.get_model.return_value = Mock(model=mock_model_response)

        model = Model(
            client=mock_client,
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )

        # Test client property
        new_client = Mock(spec=InstillClient)
        model.client = new_client
        assert model.client == new_client

        # Test resource property
        new_resource = Mock()
        model.resource = new_resource
        assert model.resource == new_resource

    def test_model_update(mock_client, mock_model_response):
        """Test Model _update method."""
        # Setup
        mock_client.model.get_model.return_value = Mock(model=mock_model_response)
        updated_model = Mock()
        updated_model.id = "updated-model-id"
        mock_client.model.get_model.side_effect = [
            Mock(model=mock_model_response),  # First call for initialization
            Mock(model=updated_model),  # Second call for _update
        ]

        model = Model(
            client=mock_client,
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )

        # Execute
        model._update()

        # Assert
        assert model.resource == updated_model
        assert mock_client.model.get_model.call_count == 2

    def test_model_get_definition(mock_client, mock_model_response):
        """Test Model get_definition method."""
        # Setup
        mock_definition = Mock()
        mock_model_response.model_definition = mock_definition
        mock_client.model.get_model.return_value = Mock(model=mock_model_response)

        model = Model(
            client=mock_client,
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )

        # Execute
        result = model.get_definition()

        # Assert
        assert result == mock_definition

    def test_model_delete(mock_client, mock_model_response):
        """Test Model delete method."""
        # Setup
        mock_client.model.get_model.return_value = Mock(model=mock_model_response)

        model = Model(
            client=mock_client,
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )

        # Execute
        model.delete(silent=True)

        # Assert
        mock_client.model.delete_model.assert_called_once_with(
            "test-model-id", silent=True
        )

    def test_model_delete_no_resource(mock_client, mock_model_response):
        """Test Model delete method when resource is None."""
        # Setup
        mock_client.model.get_model.return_value = Mock(model=mock_model_response)

        model = Model(
            client=mock_client,
            name="test-model",
            definition="test-definition",
            configuration={"key": "value"},
        )
        model.resource = None

        # Execute (should not raise exception)
        model.delete(silent=True)

        # Assert
        mock_client.model.delete_model.assert_not_called()


def describe_pipeline():
    """Test the Pipeline resource class."""

    @pytest.fixture
    def mock_client():
        """Create a mock InstillClient."""
        client = Mock(spec=InstillClient)
        client.pipeline = Mock()
        return client

    @pytest.fixture
    def mock_pipeline_response():
        """Create a mock pipeline response."""
        pipeline = Mock()
        pipeline.id = "test-pipeline-id"
        pipeline.recipe = Struct()
        return pipeline

    def test_pipeline_initialization_existing_pipeline(
        mock_client, mock_pipeline_response
    ):
        """Test Pipeline initialization when pipeline already exists."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )

        # Execute
        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Assert
        assert pipeline.client == mock_client
        assert pipeline.resource == mock_pipeline_response
        mock_client.pipeline.get_pipeline.assert_called_once_with(
            namespace_id="test-namespace", pipeline_id="test-pipeline"
        )
        mock_client.pipeline.create_pipeline.assert_not_called()

    def test_pipeline_initialization_new_pipeline(mock_client, mock_pipeline_response):
        """Test Pipeline initialization when creating new pipeline."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = None
        mock_client.pipeline.create_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )

        # Execute
        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Assert
        assert pipeline.client == mock_client
        assert pipeline.resource == mock_pipeline_response
        mock_client.pipeline.get_pipeline.assert_called_once_with(
            namespace_id="test-namespace", pipeline_id="test-pipeline"
        )
        mock_client.pipeline.create_pipeline.assert_called_once_with(
            namespace_id="test-namespace", recipe=None
        )

    def test_pipeline_initialization_with_recipe(mock_client, mock_pipeline_response):
        """Test Pipeline initialization with recipe."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = None
        mock_client.pipeline.create_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )
        recipe = Struct()

        # Execute
        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
            recipe=recipe,
        )

        # Assert
        mock_client.pipeline.create_pipeline.assert_called_once_with(
            namespace_id="test-namespace", recipe=recipe
        )

    def test_pipeline_initialization_creation_failed(mock_client):
        """Test Pipeline initialization when pipeline creation fails."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = None
        mock_client.pipeline.create_pipeline.return_value = Mock(pipeline=None)

        # Execute & Assert
        with pytest.raises(BaseException, match="pipeline creation failed"):
            Pipeline(
                client=mock_client,
                namespace_id="test-namespace",
                pipeline_id="test-pipeline",
            )

    def test_pipeline_call_success(mock_client, mock_pipeline_response):
        """Test Pipeline __call__ method with successful response."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )
        mock_response = Mock()
        mock_response.outputs = ["output1", "output2"]
        mock_response.metadata = Mock()
        mock_client.pipeline.trigger.return_value = mock_response

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        result = pipeline(task_inputs=["input1"], silent=False)

        # Assert
        assert result == (["output1", "output2"], mock_response.metadata)
        mock_client.pipeline.trigger.assert_called_once_with(
            "test-pipeline-id", ["input1"], silent=False
        )

    def test_pipeline_call_no_response(mock_client, mock_pipeline_response):
        """Test Pipeline __call__ method with no response."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )
        mock_client.pipeline.trigger.return_value = None

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        result = pipeline(task_inputs=["input1"], silent=True)

        # Assert
        assert result is None
        mock_client.pipeline.trigger.assert_called_once_with(
            "test-pipeline-id", ["input1"], silent=True
        )

    def test_pipeline_properties(mock_client, mock_pipeline_response):
        """Test Pipeline property getters and setters."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Test client property
        new_client = Mock(spec=InstillClient)
        pipeline.client = new_client
        assert pipeline.client == new_client

        # Test resource property
        new_resource = Mock()
        pipeline.resource = new_resource
        assert pipeline.resource == new_resource

    def test_pipeline_update(mock_client, mock_pipeline_response):
        """Test Pipeline _update method."""
        # Setup
        updated_pipeline = Mock()
        updated_pipeline.id = "updated-pipeline-id"

        # Create a new mock client to avoid conflicts
        fresh_mock_client = Mock(spec=InstillClient)
        fresh_mock_client.pipeline = Mock()

        # Configure the mock to handle different call signatures
        def mock_get_pipeline(*args, **kwargs):
            if "namespace_id" in kwargs and "pipeline_id" in kwargs:
                # Initialization call
                return Mock(pipeline=mock_pipeline_response)
            if "name" in kwargs:
                # Update call - return the updated pipeline directly
                return updated_pipeline
            return None

        fresh_mock_client.pipeline.get_pipeline.side_effect = mock_get_pipeline

        pipeline = Pipeline(
            client=fresh_mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        pipeline._update()

        # Assert
        assert pipeline.resource == updated_pipeline
        assert fresh_mock_client.pipeline.get_pipeline.call_count == 2

    def test_pipeline_get_operation_success(mock_client, mock_pipeline_response):
        """Test Pipeline get_operation method with successful response."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )
        mock_operation = Operation()
        mock_response = Mock()
        mock_response.operation = mock_operation
        mock_client.pipeline.get_operation.return_value = mock_response

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        result = pipeline.get_operation(mock_operation, silent=True)

        # Assert
        assert result == mock_operation
        mock_client.pipeline.get_operation.assert_called_once_with(
            mock_operation.name, silent=True
        )

    def test_pipeline_get_operation_no_response(mock_client, mock_pipeline_response):
        """Test Pipeline get_operation method with no response."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )
        mock_operation = Operation()
        mock_client.pipeline.get_operation.return_value = None

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        result = pipeline.get_operation(mock_operation, silent=False)

        # Assert
        assert result is None
        mock_client.pipeline.get_operation.assert_called_once_with(
            mock_operation.name, silent=False
        )

    def test_pipeline_trigger_async_success(mock_client, mock_pipeline_response):
        """Test Pipeline trigger_async method with successful response."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )
        mock_operation = Operation()
        mock_response = Mock()
        mock_response.operation = mock_operation
        mock_client.pipeline.trigger_async.return_value = mock_response

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        result = pipeline.trigger_async(task_inputs=["input1"], silent=True)

        # Assert
        assert result == mock_operation
        mock_client.pipeline.trigger_async.assert_called_once_with(
            "test-pipeline-id", ["input1"], silent=True
        )

    def test_pipeline_trigger_async_no_response(mock_client, mock_pipeline_response):
        """Test Pipeline trigger_async method with no response."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )
        mock_client.pipeline.trigger_async.return_value = None

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        result = pipeline.trigger_async(task_inputs=["input1"], silent=False)

        # Assert
        assert result is None
        mock_client.pipeline.trigger_async.assert_called_once_with(
            "test-pipeline-id", ["input1"], silent=False
        )

    @patch("instill.resources.pipeline.json_format.MessageToDict")
    def test_pipeline_get_recipe(mock_json_format, mock_client, mock_pipeline_response):
        """Test Pipeline get_recipe method."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )
        mock_json_format.return_value = {"recipe": "data"}

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        result = pipeline.get_recipe()

        # Assert
        assert result == {"recipe": "data"}
        mock_json_format.assert_called_once_with(mock_pipeline_response.recipe)

    def test_pipeline_update_recipe(mock_client, mock_pipeline_response):
        """Test Pipeline update_recipe method."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )
        updated_pipeline = Mock()
        mock_client.pipeline.get_pipeline.side_effect = [
            Mock(pipeline=mock_pipeline_response),  # First call for initialization
            Mock(pipeline=updated_pipeline),  # Second call for _update
        ]

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        recipe = Struct()

        # Execute
        pipeline.update_recipe(recipe, silent=True)

        # Assert
        mock_client.pipeline.update_pipeline.assert_called_once()
        call_args = mock_client.pipeline.update_pipeline.call_args
        assert call_args[0][0] == mock_pipeline_response
        assert isinstance(call_args[0][1], FieldMask)
        assert call_args[0][1].paths == ["recipe"]
        assert call_args[1]["silent"] is True

    @patch("instill.resources.pipeline.Logger")
    def test_pipeline_validate_pipeline_failure(
        mock_logger, mock_client, mock_pipeline_response
    ):
        """Test Pipeline validate_pipeline method with validation failure."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )

        # Create a proper RpcError exception
        class MockRpcError(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INVALID_ARGUMENT

            def details(self):
                return "Validation failed"

        # Set the side_effect to raise the exception
        mock_client.pipeline.validate_pipeline.side_effect = MockRpcError()

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        result = pipeline.validate_pipeline(silent=False)

        # Verify
        assert result is False
        mock_client.pipeline.validate_pipeline.assert_called_once_with(
            name="test-pipeline-id", silent=False
        )
        mock_logger.w.assert_called()

    def test_pipeline_delete(mock_client, mock_pipeline_response):
        """Test Pipeline delete method."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )

        # Execute
        pipeline.delete(silent=True)

        # Assert
        mock_client.pipeline.delete_pipeline.assert_called_once_with(
            "test-pipeline-id", silent=True
        )

    def test_pipeline_delete_no_resource(mock_client, mock_pipeline_response):
        """Test Pipeline delete method when resource is None."""
        # Setup
        mock_client.pipeline.get_pipeline.return_value = Mock(
            pipeline=mock_pipeline_response
        )

        pipeline = Pipeline(
            client=mock_client,
            namespace_id="test-namespace",
            pipeline_id="test-pipeline",
        )
        pipeline.resource = None

        # Execute (should not raise exception)
        pipeline.delete(silent=True)

        # Assert
        mock_client.pipeline.delete_pipeline.assert_not_called()
