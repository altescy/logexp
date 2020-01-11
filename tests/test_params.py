from logexp.params import Params


class TestParams:
    def setup(self):
        self.params = Params({"foo": 123})

    def test_set_and_get(self):
        self.params["bar"] = "abc"

        assert self.params["foo"] == 123
        assert self.params["bar"] == "abc"

    def test_to_json(self):
        params_json = self.params.to_json()

        assert isinstance(params_json, dict)
        assert params_json["foo"] == 123
