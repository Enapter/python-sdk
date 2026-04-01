from enapter.http.api.telemetry.labels import Labels


def test_parse_multiple_labels():
    s = "device=foo telemetry=bar custom=baz"
    labels = Labels.parse(s)
    assert labels == {"device": "foo", "telemetry": "bar", "custom": "baz"}
    assert labels.device == "foo"
    assert labels.telemetry == "bar"


def test_parse_single_label():
    s = "device=only"
    labels = Labels.parse(s)
    assert labels == {"device": "only"}
    assert labels.device == "only"
