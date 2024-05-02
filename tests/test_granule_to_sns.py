import boto3
import pytest

from granule_to_sns import generate_message, granule_to_sns


@pytest.fixture
def event():
    return {
        "input": {
            "granules": [
                {
                    "granuleId": "foo",
                    "dataType": "bar",
                    "version": "1.0",
                    "provider": "ASFDAAC",
                    "files": [
                        {
                            "size": 162946863,
                            "bucket": "data-bucket",
                            "key": "foo.h5",
                            "source": "foo.h5",
                            "fileName": "foo.h5", "type": "data",
                            "checksumType": "md5", "checksum": "a88dda7180fc2738fe42af65721577d6",
                        },
                        {
                            "size": 32,
                            "bucket": "data-bucket",
                            "key": "foo.h5.md5",
                            "source": "foo.h5.md5",
                            "fileName": "foo.h5.md5",
                            "type": "metadata", "checksumType": "md5", "checksum": "228d1f939face34465b26fbf4056898f",
                        },
                        {
                            "size": 200178,
                            "bucket": "data-bucket",
                            "key": "foo.iso.xml",
                            "source": "foo.iso.xml",
                            "fileName": "foo.iso.xml",
                            "type": "metadata", "checksumType": "md5", "checksum": "b8d18182e9ec0c781430babcdeafaea9",
                        },
                        {
                            "size": 32,
                            "bucket": "data-bucket",
                            "key": "foo.iso.xml.md5",
                            "source": "foo.iso.xml.md5",
                            "fileName": "foo.iso.xml.md5",
                            "type": "metadata", "checksumType": "md5", "checksum": "aef479deb833175bbfcfb048a0f4d06e",
                        },
                        {
                            "bucket": "data-bucket",
                            "key": "UMMG/foo.cmr.json",
                            "fileName": "foo.cmr.json",
                        },
                    ],
                },
            ],
        },
    }


@pytest.fixture
def message():
    return {
        "identifier": "foo",
        "collection": "bar",
        "product": {
            "name": "foo",
            "files": [
                {
                    "name": "foo.h5",
                    "uri": "s3://data-bucket/foo.h5",
                },
                {
                    "name": "foo.h5.md5",
                    "uri": "s3://data-bucket/foo.h5.md5",
                },
                {
                    "name": "foo.iso.xml",
                    "uri": "s3://data-bucket/foo.iso.xml",
                },
                {
                    "name": "foo.iso.xml.md5",
                    "uri": "s3://data-bucket/foo.iso.xml.md5",
                },
                {
                    "name": "foo.cmr.json",
                    "uri": "s3://data-bucket/UMMG/foo.cmr.json",
                },
            ],
        },
    }


@pytest.fixture
def sns_client(mocker):
    sns_client = boto3.client("sns", region_name="us-west-2")
    mocker.patch("boto3.client", return_value=sns_client)
    return sns_client


def test_generate_message(event, message):
    assert generate_message(event["input"]["granules"][0]) == message


def test_granule_to_sns(sns_client, event, mocker):
    mocker.patch.object(sns_client, "publish", return_value={})
    assert granule_to_sns(event, None) == event
