import importlib.util
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


LAMBDA_PATH = (
    Path(__file__).resolve().parents[1]
    / "terraform"
    / "lambda"
    / "remediate_s3_public.py"
)


mock_s3 = MagicMock()

with patch("boto3.client", return_value=mock_s3):
    spec = importlib.util.spec_from_file_location(
        "remediate_s3_public",
        LAMBDA_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

lambda_handler = module.lambda_handler


def test_remediates_bucket_from_direct_event():
    mock_s3.reset_mock()

    event = {"bucket_name": "test-bucket"}

    result = lambda_handler(event, None)

    mock_s3.put_public_access_block.assert_called_once_with(
        Bucket="test-bucket",
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )

    assert result["statusCode"] == 200
    assert result["bucket"] == "test-bucket"
    assert result["action"] == "public_access_block_enforced"


def test_remediates_bucket_from_config_event():
    mock_s3.reset_mock()

    event = {
        "detail": {
            "resourceId": "config-test-bucket"
        }
    }

    result = lambda_handler(event, None)

    mock_s3.put_public_access_block.assert_called_once()

    assert result["bucket"] == "config-test-bucket"


def test_missing_bucket_name_raises_error():
    mock_s3.reset_mock()

    with pytest.raises(ValueError, match="Missing S3 bucket name"):
        lambda_handler({}, None)

    mock_s3.put_public_access_block.assert_not_called()
