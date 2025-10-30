# pylint: disable=no-member,wrong-import-position,too-many-lines,no-name-in-module
import base64
import os

import instill.protogen.artifact.artifact.v1alpha.file_pb2 as file_interface


def get_file_type(file_path, file_extension):
    # Dictionary mapping file extensions to file type enum values
    extension_mapping = {
        ".pdf": file_interface.File.TYPE_PDF,
        ".html": file_interface.File.TYPE_HTML,
        ".htm": file_interface.File.TYPE_HTML,
        ".md": file_interface.File.TYPE_MARKDOWN,
        ".markdown": file_interface.File.TYPE_MARKDOWN,
        ".doc": file_interface.File.TYPE_DOC,
        ".docx": file_interface.File.TYPE_DOCX,
        ".ppt": file_interface.File.TYPE_PPT,
        ".pptx": file_interface.File.TYPE_PPTX,
        ".xls": file_interface.File.TYPE_XLS,
        ".xlsx": file_interface.File.TYPE_XLSX,
        ".txt": file_interface.File.TYPE_TEXT,
        ".log": file_interface.File.TYPE_TEXT,
        ".ini": file_interface.File.TYPE_TEXT,
        ".csv": file_interface.File.TYPE_CSV,
    }

    # Check if the file extension is in our mapping
    file_type = extension_mapping.get(file_extension.lower(), None)

    # If file type is unknown, try to guess based on content
    if file_type is None:
        with open(file_path, "rb") as file:
            content = file.read(4096)  # Read first 4KB of the file

            # Check for PDF signature
            if content.startswith(b"%PDF-"):
                file_type = file_interface.File.TYPE_PDF
            # Check for HTML signature
            elif b"<!DOCTYPE html>" in content.lower() or b"<html" in content.lower():
                file_type = file_interface.File.TYPE_HTML
            # Check for Office Open XML formats (DOCX, PPTX, XLSX)
            elif content.startswith(b"PK\x03\x04"):
                if "[Content_Types].xml" in str(content) and "word/" in str(content):
                    file_type = file_interface.File.TYPE_DOCX
                elif "[Content_Types].xml" in str(content) and "ppt/" in str(content):
                    file_type = file_interface.File.TYPE_PPTX
                elif "[Content_Types].xml" in str(content) and "xl/" in str(content):
                    file_type = file_interface.File.TYPE_XLSX

    if file_type is None:
        raise ValueError(f"Unsupported file type: {file_extension}")

    return file_type


def process_file(file_path) -> file_interface.File:
    # Check if the file path exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    # Get file name and extension
    file_name = os.path.basename(file_path)
    _, file_extension = os.path.splitext(file_name)

    # Check file type
    file_type = get_file_type(file_path, file_extension)

    # Read file content and encode to base64
    with open(file_path, "rb") as file:
        file_content = file.read()
        base64_encoded = base64.b64encode(file_content).decode("utf-8")

    return file_interface.File(
        filename=file_name, type=file_type, content=base64_encoded
    )


# Example usage
# file_path = "/tmp/example.pdf"
# result = process_file(file_path)
# print(result.name)
# print((result.type))
