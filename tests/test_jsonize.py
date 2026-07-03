import json
import os
import subprocess
import sys
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jsonize")


def run(args, stdin=None):
    proc = subprocess.run(
        [sys.executable, SCRIPT, *args],
        input=stdin,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.strip("\n"), proc.stderr


class TestObjectMode(unittest.TestCase):
    def test_basic_types(self):
        code, out, _ = run(["name=jsonize", "count=17", "stable=false"], stdin="")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"name": "jsonize", "count": 17, "stable": False})

    def test_missing_value_is_null(self):
        code, out, _ = run(["nada="], stdin="")
        self.assertEqual(json.loads(out), {"nada": None})

    def test_bad_float_becomes_string(self):
        code, out, _ = run(["badfloat=3.14159.26"], stdin="")
        self.assertEqual(json.loads(out), {"badfloat": "3.14159.26"})

    def test_whole_float_drops_decimal(self):
        code, out, _ = run(["a=1.0"], stdin="")
        self.assertEqual(out, '{"a":1}')

    def test_boolean_shorthand(self):
        code, out, _ = run(["switch=true", "morning@0", "coffee@T"], stdin="")
        self.assertEqual(json.loads(out), {"switch": True, "morning": False, "coffee": True})

    def test_no_literals_flag(self):
        code, out, _ = run(["-B", "switch=true", "morning@0"], stdin="")
        self.assertEqual(json.loads(out), {"switch": "true", "morning": False})

    def test_no_empty_flag_skips_key(self):
        code, out, _ = run(["-n", "a=", "b=1"], stdin="")
        self.assertEqual(json.loads(out), {"b": 1})

    def test_duplicate_keys_kept_by_default(self):
        code, out, _ = run(["a=1", "b=2", "a=3"], stdin="")
        self.assertEqual(out, '{"a":1,"b":2,"a":3}')

    def test_dedupe_flag(self):
        code, out, _ = run(["-D", "a=1", "b=2", "a=3"], stdin="")
        self.assertEqual(out, '{"a":3,"b":2}')


class TestArrayMode(unittest.TestCase):
    def test_basic_array(self):
        code, out, _ = run(["-a", "1", "2", "3"], stdin="")
        self.assertEqual(json.loads(out), [1, 2, 3])

    def test_empty_array(self):
        code, out, _ = run(["-a"], stdin="")
        self.assertEqual(out, "[]")


class TestNestedPaths(unittest.TestCase):
    def test_bracket_object_and_array(self):
        code, out, _ = run(
            ["name=Jane", "point[]=1", "point[]=2", "geo[lat]=10", "geo[lon]=20"], stdin=""
        )
        self.assertEqual(
            json.loads(out),
            {"name": "Jane", "point": [1, 2], "geo": {"lat": 10, "lon": 20}},
        )

    def test_dot_path_with_delim(self):
        code, out, _ = run(["-d.", "geo.lat=10", "geo.lon=20"], stdin="")
        self.assertEqual(json.loads(out), {"geo": {"lat": 10, "lon": 20}})

    def test_dot_is_literal_without_delim(self):
        code, out, _ = run(["geo.lat=10"], stdin="")
        self.assertEqual(json.loads(out), {"geo.lat": 10})


class TestCoercionOverrides(unittest.TestCase):
    def test_matrix(self):
        code, out, _ = run(
            [
                "--",
                "-s", "a=true",
                "b=true",
                "-s", "c=123",
                "d=123",
                "-b", "e=1",
                "-b", "f=true",
                "-n", "g=This is a test",
                "-b", "h=This is a test",
            ],
            stdin="",
        )
        self.assertEqual(
            json.loads(out),
            {
                "a": "true",
                "b": True,
                "c": "123",
                "d": 123,
                "e": True,
                "f": True,
                "g": 14,
                "h": True,
            },
        )


class TestEscaping(unittest.TestCase):
    def test_escaped_at_sign(self):
        code, out, _ = run(["twitter=\\@jpmens"], stdin="")
        self.assertEqual(json.loads(out), {"twitter": "@jpmens"})


class TestFileOperators(unittest.TestCase):
    def setUp(self):
        self.tmp = "jsonize_test_tmp.txt"
        with open(self.tmp, "w") as f:
            f.write("hello file")

    def tearDown(self):
        os.remove(self.tmp)

    def test_at_file_raw(self):
        code, out, _ = run([f"content=@{self.tmp}"], stdin="")
        self.assertEqual(json.loads(out), {"content": "hello file"})

    def test_percent_file_base64(self):
        code, out, _ = run([f"content=%{self.tmp}"], stdin="")
        import base64
        self.assertEqual(json.loads(out)["content"], base64.b64encode(b"hello file").decode())


class TestMergeAndFile(unittest.TestCase):
    def test_coloneq_and_dash_f(self):
        code, out, _ = run(["-a", "a", "b", "c"], stdin="")
        with open("jsonize_child.json", "w") as f:
            f.write(out)
        try:
            code, out2, _ = run(["files:=jsonize_child.json"], stdin="")
            self.assertEqual(json.loads(out2), {"files": ["a", "b", "c"]})

            code, out3, _ = run(["-f", "jsonize_child.json", "1", "2"], stdin="")
            self.assertEqual(json.loads(out3), ["a", "b", "c", 1, 2])
        finally:
            os.remove("jsonize_child.json")


class TestStdin(unittest.TestCase):
    def test_words_from_stdin(self):
        code, out, _ = run(["-a"], stdin="1\n2\n3\n")
        self.assertEqual(json.loads(out), [1, 2, 3])

    def test_empty_stdin_object(self):
        code, out, err = run([], stdin="")
        self.assertEqual(out, "{}")


class TestPrettyPrint(unittest.TestCase):
    def test_pretty_output(self):
        code, out, _ = run(["-p", "a=1"], stdin="")
        self.assertEqual(out, '{\n  "a": 1\n}')


if __name__ == "__main__":
    unittest.main()
