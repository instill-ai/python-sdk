"""Unit tests for CLI commands."""

# pylint: disable=unused-argument

import os
import subprocess
import tempfile
from unittest.mock import MagicMock, mock_open, patch

import pytest

from instill.helpers.cli import cli
from instill.helpers.commands.build import add_build_parser, build
from instill.helpers.commands.init import add_init_parser, init
from instill.helpers.commands.push import add_push_parser, push
from instill.helpers.commands.run import add_run_parser, run
from instill.helpers.commands.utils import (
    config_check_required_fields,
    find_project_root,
    parse_image_tag_name,
    parse_target_arch,
    prepare_build_command,
    prepare_build_environment,
    validate_cuda_version,
    validate_python_version,
)
from instill.helpers.errors import ModelConfigException


class TestInitCommand:
    """Test cases for the init command."""

    def test_add_init_parser(self):
        """Test that init parser is added correctly."""
        subcommands = MagicMock()
        add_init_parser(subcommands)

        subcommands.add_parser.assert_called_once_with(
            "init", help="Initialize model directory"
        )
        parser = subcommands.add_parser.return_value
        parser.set_defaults.assert_called_once_with(func=init)

    @patch("instill.helpers.commands.init.shutil.copyfile")
    @patch("instill.helpers.commands.init.os.getcwd")
    @patch("instill.helpers.commands.init.__file__")
    @patch("instill.helpers.commands.init.Logger")
    def test_init_success(self, mock_logger, mock_file, mock_getcwd, mock_copyfile):
        """Test successful initialization."""
        mock_file.return_value = "/path/to/commands/init.py"
        mock_getcwd.return_value = "/current/dir"

        args = MagicMock()
        init(args)

        # Check that files were copied
        assert mock_copyfile.call_count == 2

        # Check that success message was logged
        mock_logger.i.assert_called_once_with(
            "[Instill] Model directory initialized successfully"
        )

    @patch("instill.helpers.commands.init.shutil.copyfile")
    @patch("instill.helpers.commands.init.os.getcwd")
    @patch("instill.helpers.commands.init.__file__")
    @patch("instill.helpers.commands.init.Logger")
    def test_init_file_not_found(
        self, mock_logger, mock_file, mock_getcwd, mock_copyfile
    ):
        """Test init when template files are not found."""
        mock_file.return_value = "/path/to/commands/init.py"
        mock_getcwd.return_value = "/current/dir"
        mock_copyfile.side_effect = FileNotFoundError("Template not found")

        args = MagicMock()
        init(args)  # Should not raise exception, just log error

        # Check that error was logged
        mock_logger.e.assert_called()
        error_calls = [
            call
            for call in mock_logger.e.call_args_list
            if "[Instill] Failed to initialize model directory" in str(call)
        ]
        assert len(error_calls) == 1

    @patch("instill.helpers.commands.init.shutil.copyfile")
    @patch("instill.helpers.commands.init.os.getcwd")
    @patch("instill.helpers.commands.init.Logger")
    def test_init_permission_error(self, mock_logger, mock_getcwd, mock_copyfile):
        """Test init when there's a permission error."""
        mock_getcwd.return_value = "/current/dir"
        mock_copyfile.side_effect = PermissionError("Permission denied")

        args = MagicMock()
        init(args)  # Should not raise exception, just log error

        # Check that error was logged
        mock_logger.e.assert_called()
        error_calls = [
            call
            for call in mock_logger.e.call_args_list
            if "[Instill] Failed to initialize model directory" in str(call)
        ]
        assert len(error_calls) == 1


class TestBuildCommand:
    """Test cases for the build command."""

    def test_add_build_parser(self):
        """Test that build parser is added correctly."""
        subcommands = MagicMock()
        add_build_parser(subcommands, "amd64")

        subcommands.add_parser.assert_called_once_with(
            "build", help="Build model image"
        )
        parser = subcommands.add_parser.return_value
        assert parser.add_argument.call_count == 5

    @patch("instill.helpers.commands.build.Logger")
    @patch("instill.helpers.commands.build.open", new_callable=mock_open)
    def test_build_missing_config_file(self, mock_open, mock_logger):
        """Test build when config file is missing."""
        mock_open.side_effect = FileNotFoundError("Config file not found")

        args = MagicMock()
        args.name = "test/model"
        args.no_cache = False
        args.target_arch = "amd64"
        args.sdk_wheel = None
        args.editable_project = None

        build(args)  # Should not raise exception, just log error

        # Check that error was logged
        mock_logger.e.assert_called()
        error_calls = [
            call
            for call in mock_logger.e.call_args_list
            if "Config file not found" in str(call)
        ]
        assert len(error_calls) == 1

    @patch("instill.helpers.commands.build.open", new_callable=mock_open)
    @patch("instill.helpers.commands.build.Logger")
    @patch("instill.helpers.commands.build.yaml.safe_load")
    def test_build_invalid_config(self, mock_logger, mock_yaml_load, mock_open):
        """Test build with invalid configuration."""
        mock_yaml_load.return_value = {"build": {"gpu": None}}

        args = MagicMock()
        args.name = "test/model"
        args.no_cache = False
        args.target_arch = "amd64"
        args.sdk_wheel = None
        args.editable_project = None

        with pytest.raises(ModelConfigException):
            build(args)

    @patch("instill.helpers.commands.build.open", new_callable=mock_open)
    @patch("instill.helpers.commands.build.Logger")
    @patch("instill.helpers.commands.build.yaml.safe_load")
    def test_build_gpu_on_arm64(self, mock_yaml_load, mock_logger, mock_open):
        """Test build with GPU on ARM64 architecture."""
        mock_yaml_load.return_value = {
            "build": {"gpu": True, "llm_runtime": "transformers"}
        }

        args = MagicMock()
        args.name = "test/model"
        args.no_cache = False
        args.target_arch = "arm64"
        args.sdk_wheel = None
        args.editable_project = None

        build(args)  # Should not raise exception, just log error

        # Check that error was logged
        mock_logger.e.assert_called()
        error_calls = [
            call
            for call in mock_logger.e.call_args_list
            if "GPU is not supported on ARM64 architecture" in str(call)
        ]
        assert len(error_calls) == 1

    @patch("subprocess.run")
    @patch("instill.helpers.commands.build.open", new_callable=mock_open)
    @patch("instill.helpers.commands.build.shutil.copytree")
    @patch("instill.helpers.commands.build.shutil.copyfile")
    @patch("instill.helpers.commands.build.os.getcwd")
    @patch("instill.helpers.commands.build.tempfile.TemporaryDirectory")
    @patch("instill.helpers.commands.build.yaml.safe_load")
    @patch("instill.helpers.commands.build.Logger")
    def test_build_with_sdk_wheel(
        self,
        mock_logger,
        mock_yaml_load,
        mock_tempdir,
        mock_getcwd,
        mock_copyfile,
        mock_copytree,
        mock_open,
        mock_subprocess,
    ):
        """Test build with SDK wheel."""
        mock_yaml_load.return_value = {
            "build": {"gpu": False, "llm_runtime": "transformers"}
        }

        mock_tempdir.return_value.__enter__.return_value = "/tmp/test"
        mock_subprocess.return_value.returncode = 0
        mock_getcwd.return_value = "/current/working/dir"

        args = MagicMock()
        args.name = "test/model"
        args.no_cache = False
        args.target_arch = "amd64"
        args.sdk_wheel = "/path/to/instill_sdk-0.17.2-py3-none-any.whl"
        args.editable_project = None

        build(args)

        # Verify SDK wheel was copied - check for any wheel copy call
        wheel_calls = [
            call
            for call in mock_copyfile.call_args_list
            if "instill_sdk" in str(call) and "dev-py3-none-any.whl" in str(call)
        ]
        assert (
            len(wheel_calls) == 1
        ), f"Expected 1 wheel copy call, found {len(wheel_calls)}"

        # Verify other expected copy operations occurred
        # Check that dockerfile was copied
        dockerfile_calls = [
            call
            for call in mock_copyfile.call_args_list
            if "Dockerfile.transformers" in str(call)
        ]
        assert len(dockerfile_calls) == 1

        # Check that .dockerignore was copied
        dockerignore_calls = [
            call
            for call in mock_copyfile.call_args_list
            if ".dockerignore" in str(call)
        ]
        assert len(dockerignore_calls) == 1

        # Check that model.py was copied as _model.py
        model_calls = [
            call for call in mock_copyfile.call_args_list if "_model.py" in str(call)
        ]
        assert len(model_calls) == 1

        # Verify the build command was executed
        mock_subprocess.assert_called_once()
        build_call = mock_subprocess.call_args[0][0]
        assert build_call[0] == "docker"
        assert build_call[1] == "buildx"
        assert build_call[2] == "build"

    @patch("instill.helpers.commands.build.open", new_callable=mock_open)
    @patch("instill.helpers.commands.build.find_project_root")
    @patch("instill.helpers.commands.build.subprocess.run")
    @patch("instill.helpers.commands.build.shutil.copytree")
    @patch("instill.helpers.commands.build.shutil.copyfile")
    @patch("instill.helpers.commands.build.os.getcwd")
    @patch("instill.helpers.commands.build.tempfile.TemporaryDirectory")
    @patch("instill.helpers.commands.build.yaml.safe_load")
    @patch("instill.helpers.commands.build.Logger")
    def test_build_with_editable_project(
        self,
        mock_logger,
        mock_yaml_load,
        mock_tempdir,
        mock_getcwd,
        mock_copyfile,
        mock_copytree,
        mock_subprocess,
        mock_find_project_root,
        mock_open,
    ):
        """Test build with editable project."""
        mock_yaml_load.return_value = {
            "build": {"gpu": False, "llm_runtime": "transformers"}
        }

        mock_tempdir.return_value.__enter__.return_value = "/tmp/test"
        mock_subprocess.return_value.returncode = 0
        mock_getcwd.return_value = "/current/working/dir"

        # Mock the project root finding
        mock_find_project_root.return_value = "/path/to/project"

        args = MagicMock()
        args.name = "test/model"
        args.no_cache = False
        args.target_arch = "amd64"
        args.sdk_wheel = None
        args.editable_project = "/path/to/project"

        build(args)

        # Verify project was copied - use the correct path based on os.path.basename
        mock_copytree.assert_any_call(
            "/path/to/project", "/tmp/test/project", dirs_exist_ok=True
        )

    @patch("instill.helpers.commands.build.open", new_callable=mock_open)
    @patch("instill.helpers.commands.build.find_project_root")
    @patch("instill.helpers.commands.build.subprocess.run")
    @patch("instill.helpers.commands.build.shutil.copytree")
    @patch("instill.helpers.commands.build.shutil.copyfile")
    @patch("instill.helpers.commands.build.os.getcwd")
    @patch("instill.helpers.commands.build.tempfile.TemporaryDirectory")
    @patch("instill.helpers.commands.build.yaml.safe_load")
    @patch("instill.helpers.commands.build.Logger")
    def test_build_with_editable_project_custom_name(
        self,
        mock_logger,
        mock_yaml_load,
        mock_tempdir,
        mock_getcwd,
        mock_copyfile,
        mock_copytree,
        mock_subprocess,
        mock_find_project_root,
        mock_open,
    ):
        """Test build with editable project that has a custom name."""
        mock_yaml_load.return_value = {
            "build": {"gpu": False, "llm_runtime": "transformers"}
        }

        mock_tempdir.return_value.__enter__.return_value = "/tmp/test"
        mock_subprocess.return_value.returncode = 0
        mock_getcwd.return_value = "/current/working/dir"

        # Mock the project root finding with a custom project name
        mock_find_project_root.return_value = "/path/to/my-custom-project"

        args = MagicMock()
        args.name = "test/model"
        args.no_cache = False
        args.target_arch = "amd64"
        args.sdk_wheel = None
        args.editable_project = "/path/to/my-custom-project"

        build(args)

        # Verify project was copied with the correct name
        mock_copytree.assert_any_call(
            "/path/to/my-custom-project",
            "/tmp/test/my-custom-project",
            dirs_exist_ok=True,
        )


class TestPushCommand:
    """Test cases for the push command."""

    def test_add_push_parser(self):
        """Test that push parser is added correctly."""
        subcommands = MagicMock()
        add_push_parser(subcommands)

        subcommands.add_parser.assert_called_once_with("push", help="Push model image")
        parser = subcommands.add_parser.return_value
        assert parser.add_argument.call_count == 2  # name, url

    @patch("instill.helpers.commands.push.subprocess.run")
    @patch("instill.helpers.commands.push.Logger")
    def test_push_success(self, mock_logger, mock_subprocess):
        """Test successful push operation."""
        mock_subprocess.return_value.returncode = 0

        args = MagicMock()
        args.name = "test/model"
        args.url = "registry.example.com"

        push(args)

        # Check that docker tag and push were called
        assert mock_subprocess.call_count == 3  # tag, push, rmi

        # Check that success messages were logged
        mock_logger.i.assert_called()
        success_calls = [
            call for call in mock_logger.i.call_args_list if "pushed" in str(call)
        ]
        assert len(success_calls) == 1

    @patch("instill.helpers.commands.push.subprocess.run")
    @patch("instill.helpers.commands.push.Logger")
    def test_push_failure(self, mock_logger, mock_subprocess):
        """Test push operation failure."""

        # Mock the subprocess calls to simulate failure
        def mock_run_side_effect(*args, **kwargs):
            # First call (tag) succeeds
            if "tag" in args[0]:
                return MagicMock(returncode=0)
            # Second call (push) fails
            if "push" in args[0]:
                raise subprocess.CalledProcessError(1, args[0])
            # Third call (rmi) succeeds
            if "rmi" in args[0]:
                return MagicMock(returncode=0)
            return MagicMock(returncode=0)

        mock_subprocess.side_effect = mock_run_side_effect

        args = MagicMock()
        args.name = "test/model"
        args.url = "registry.example.com"

        push(args)  # Should not raise exception, just log error

        # Check that error was logged
        mock_logger.e.assert_called()
        error_calls = [
            call
            for call in mock_logger.e.call_args_list
            if "[Instill] Push failed" in str(call)
        ]
        assert len(error_calls) == 1


class TestRunCommand:
    """Test cases for the run command."""

    def test_add_run_parser(self):
        """Test that run parser is added correctly."""
        subcommands = MagicMock()
        add_run_parser(subcommands)

        subcommands.add_parser.assert_called_once_with(
            "run", help="Run inference on model image"
        )
        parser = subcommands.add_parser.return_value
        assert (
            parser.add_argument.call_count == 6
        )  # name, num-of-cpus, cpu-kvcache-space, gpu, num-of-gpus, input

    @patch("instill.helpers.commands.run.subprocess.run")
    @patch("instill.helpers.commands.run.uuid.uuid4")
    @patch("instill.helpers.commands.run.Logger")
    def test_run_cpu_mode(self, mock_logger, mock_uuid, mock_subprocess):
        """Test run in CPU mode."""
        mock_uuid.return_value = "test-uuid"
        mock_subprocess.return_value.returncode = 0

        args = MagicMock()
        args.name = "test/model"
        args.num_of_cpus = 2
        args.cpu_kvcache_space = 8
        args.gpu = False
        args.num_of_gpus = 1
        args.input = '{"test": "data"}'

        run(args)

        # Check that docker run was called with CPU parameters
        calls = mock_subprocess.call_args_list
        docker_run_call = calls[0][0][0]

        assert docker_run_call[0] == "docker"
        assert docker_run_call[1] == "run"
        assert "-d" in docker_run_call
        assert "--privileged" in docker_run_call
        assert "--shm-size=4gb" in docker_run_call
        assert "--rm" in docker_run_call
        assert "--name" in docker_run_call
        assert "test-uuid" in docker_run_call
        assert "test/model:latest" in docker_run_call

    @patch("instill.helpers.commands.run.subprocess.run")
    @patch("instill.helpers.commands.run.uuid.uuid4")
    @patch("instill.helpers.commands.run.Logger")
    def test_run_gpu_mode(self, mock_logger, mock_uuid, mock_subprocess):
        """Test run in GPU mode."""
        mock_uuid.return_value = "test-uuid"
        mock_subprocess.return_value.returncode = 0

        args = MagicMock()
        args.name = "test/model"
        args.num_of_cpus = 1
        args.cpu_kvcache_space = 4
        args.gpu = True
        args.num_of_gpus = 2
        args.input = '{"test": "data"}'

        run(args)

        # Check that docker run was called with GPU parameters
        calls = mock_subprocess.call_args_list
        docker_run_call = calls[0][0][0]

        assert docker_run_call[0] == "docker"
        assert docker_run_call[1] == "run"
        assert "--device" in docker_run_call
        assert "nvidia.com/gpu:2" in docker_run_call


class TestUtils:
    """Test cases for utility functions."""

    def test_config_check_required_fields_valid(self):
        """Test config check with valid configuration."""
        config = {"build": {"gpu": True, "llm_runtime": "transformers"}}

        # Should not raise any exception
        config_check_required_fields(config)

    def test_config_check_required_fields_missing_build(self):
        """Test config check with missing build section."""
        config = {"other": "value"}

        with pytest.raises(ModelConfigException, match="build"):
            config_check_required_fields(config)

    def test_config_check_required_fields_missing_gpu(self):
        """Test config check with missing gpu field."""
        config = {"build": {"other": "value"}}

        with pytest.raises(ModelConfigException, match="gpu"):
            config_check_required_fields(config)

    def test_find_project_root_found(self):
        """Test finding project root when it exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a mock project structure
            project_dir = os.path.join(temp_dir, "test_project")
            os.makedirs(project_dir)

            # Create pyproject.toml in the project directory
            pyproject_path = os.path.join(project_dir, "pyproject.toml")
            with open(pyproject_path, "w", encoding="utf-8") as f:
                f.write("[tool.poetry]\nname = 'test'\n")

            # Test from a subdirectory
            subdir = os.path.join(project_dir, "src", "package")
            os.makedirs(subdir)

            result = find_project_root(subdir)
            assert result == project_dir

    def test_find_project_root_not_found(self):
        """Test finding project root when it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = find_project_root(temp_dir)
            assert result is None

    @pytest.mark.parametrize(
        "version,expected",
        [
            ("3.12", "312"),
            ("3.11", "311"),
            ("3.10", "310"),
            ("3.9", "39"),
            ("", "312"),  # Default
        ],
    )
    def test_validate_python_version_valid(self, version, expected):
        """Test Python version validation with valid versions."""
        result = validate_python_version(version)
        assert result == expected

    @pytest.mark.parametrize(
        "version,error_msg",
        [
            ("2.7", "too old"),
            ("3.13", "too new"),
            ("invalid", "format"),
            ("3", "format"),
        ],
    )
    def test_validate_python_version_invalid(self, version, error_msg):
        """Test Python version validation with invalid versions."""
        with pytest.raises(ValueError, match=error_msg):
            validate_python_version(version)

    @pytest.mark.parametrize(
        "version,expected",
        [
            ("12.8", "128"),
            ("12.2", "122"),
            ("", "128"),  # Default
        ],
    )
    def test_validate_cuda_version_valid(self, version, expected):
        """Test CUDA version validation with valid versions."""
        result = validate_cuda_version(version)
        assert result == expected

    @pytest.mark.parametrize(
        "version,error_msg",
        [
            ("11.8", "too old"),  # Below minimum 12.2
            ("13.0", "too new"),  # Above maximum 12.8
            ("invalid", "format"),
            ("12", "format"),
        ],
    )
    def test_validate_cuda_version_invalid(self, version, error_msg):
        """Test CUDA version validation with invalid versions."""
        with pytest.raises(ValueError, match=error_msg):
            validate_cuda_version(version)

    @patch("instill.helpers.commands.utils.ray.__version__", "2.47.0")
    @patch("instill.__version__", "0.17.2")
    def test_prepare_build_environment_cpu(self):
        """Test build environment preparation for CPU."""
        build_params = {
            "gpu": False,
            "llm_runtime": "transformers",
            "python_version": "3.12",
            "system_packages": ["git", "curl"],
            "python_packages": ["numpy", "pandas"],
        }

        result = prepare_build_environment(build_params)

        assert len(result) == 8
        (
            llm_runtime,
            ray_version,
            python_version,
            cuda_version,
            device_type,
            system_pkg_str,
            python_pkg_str,
            instill_sdk_version,
        ) = result

        assert llm_runtime == "transformers"
        assert ray_version == "2.47.0"
        assert python_version == "-py312"
        assert cuda_version == ""
        assert device_type == "-cpu"
        assert system_pkg_str == "git curl"
        assert python_pkg_str == "numpy pandas"
        assert instill_sdk_version == "0.17.2"

    @patch("instill.helpers.commands.utils.ray.__version__", "2.47.0")
    @patch("instill.__version__", "0.17.2")
    def test_prepare_build_environment_gpu(self):
        """Test build environment preparation for GPU."""
        build_params = {
            "gpu": True,
            "cuda_version": "12.8",
            "llm_runtime": "vllm",
            "python_version": "3.12",
        }

        result = prepare_build_environment(build_params)

        assert len(result) == 8
        (
            llm_runtime,
            ray_version,
            python_version,
            cuda_version,
            device_type,
            system_pkg_str,
            python_pkg_str,
            instill_sdk_version,
        ) = result

        assert llm_runtime == "vllm"
        assert ray_version == "2.47.0"
        assert python_version == "-py312"
        assert cuda_version == "-cu128"
        assert device_type == "-gpu"
        assert system_pkg_str == ""
        assert python_pkg_str == ""
        assert instill_sdk_version == "0.17.2"

    @pytest.mark.parametrize(
        "image_name,expected",
        [
            ("test/model", "test/model:latest"),
            ("test/model:latest", "test/model:latest"),
            ("test/model:v1.0", "test/model:v1.0"),
        ],
    )
    def test_parse_image_tag_name(self, image_name, expected):
        """Test image tag name parsing."""
        result = parse_image_tag_name(image_name)
        assert result == expected

    @pytest.mark.parametrize(
        "arch,expected",
        [
            ("amd64", "amd64"),
            ("arm64", "aarch64"),
        ],
    )
    def test_parse_target_arch_valid(self, arch, expected):
        """Test target architecture parsing with valid values."""
        result = parse_target_arch(arch)
        assert result == expected

    def test_parse_target_arch_invalid(self):
        """Test target architecture parsing with invalid value."""
        with pytest.raises(ValueError, match="Invalid target architecture"):
            parse_target_arch("invalid")

    def test_prepare_build_command(self):
        """Test build command preparation."""
        tmpdir = "/tmp/test"
        dockerfile = "Dockerfile.transformers"
        build_vars = [
            "test/model:latest",  # image_name_tag
            "amd64",  # target_arch
            False,  # no_cache
            "transformers",  # llm_runtime
            "2.47.0",  # ray_version
            "-py312",  # python_version
            "",  # cuda_version
            "-cpu",  # device_type
            "numpy pandas",  # python_pkg_str
            "git curl",  # system_pkg_str
            "0.17.2",  # instill_sdk_version
            None,  # instill_python_sdk_project_name
        ]

        command = prepare_build_command(tmpdir, dockerfile, build_vars)

        assert command[0] == "docker"
        assert command[1] == "buildx"
        assert command[2] == "build"
        assert "--file" in command
        assert f"{tmpdir}/{dockerfile}" in command
        assert "--platform" in command
        assert "linux/amd64" in command
        assert "-t" in command
        assert "test/model:latest" in command


class TestCLIIntegration:
    """Integration tests for CLI commands."""

    @patch("instill.helpers.cli.add_init_parser")
    @patch("instill.helpers.cli.add_build_parser")
    @patch("instill.helpers.cli.add_push_parser")
    @patch("instill.helpers.cli.add_run_parser")
    @patch("instill.helpers.cli.argparse.ArgumentParser")
    def test_cli_setup(self, mock_parser, mock_run, mock_push, mock_build, mock_init):
        """Test that CLI sets up all command parsers correctly."""
        mock_parser_instance = MagicMock()
        mock_parser.return_value = mock_parser_instance
        mock_parser_instance.add_subparsers.return_value = MagicMock()

        # Mock platform.machine to return a known value
        with patch("instill.helpers.cli.platform.machine", return_value="x86_64"):
            cli()

        # Check that all parsers were added
        mock_init.assert_called_once()
        mock_build.assert_called_once()
        mock_push.assert_called_once()
        mock_run.assert_called_once()

    def test_cli_default_platform_detection(self):
        """Test CLI platform detection."""
        with patch("instill.helpers.cli.platform.machine") as mock_machine:
            # Test x86_64 detection
            mock_machine.return_value = "x86_64"
            with patch("instill.helpers.cli.argparse.ArgumentParser") as mock_parser:
                mock_parser_instance = MagicMock()
                mock_parser.return_value = mock_parser_instance
                mock_parser_instance.add_subparsers.return_value = MagicMock()

                # Mock the parser functions to avoid the actual function calls
                with patch("instill.helpers.cli.add_init_parser"):
                    with patch("instill.helpers.cli.add_build_parser") as mock_build:
                        with patch("instill.helpers.cli.add_push_parser"):
                            with patch("instill.helpers.cli.add_run_parser"):
                                cli()

                                # Check that build parser was called with amd64
                                mock_build.assert_called_once()
                                args, _ = mock_build.call_args
                                assert (
                                    args[1] == "amd64"
                                )  # default_platform should be amd64


if __name__ == "__main__":
    pytest.main([__file__])
