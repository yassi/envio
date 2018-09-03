import os
import sys
import random
from unittest import TestCase, main

from . import get_var, EnvioParseError, BOOL_TRUE, BOOL_FALSE

class TestEnvio(TestCase):
    def setUp(self):
        """set up an array to track env variables created by a test
        """
        self.env_vars = []

    def tearDown(self):
        """Delete all env vars created by a test.
        """
        while self.env_vars:
            del os.environ[self.env_vars.pop()]

    def set_env_var(self, name, val):
        """Artificially set up an env variable by just adding it to python's
        os.environ mapping and keeping track of it in self.env_vars
        """
        os.environ[name] = val
        self.env_vars.append(name)

    def test_can_access_environment_vars(self):
        self.set_env_var('MYVAR', 'here')
        self.assertEqual(get_var('MYVAR'), 'here')

    def test_will_use_default_if_var_not_defined(self):
        expected = 'expected'
        val = get_var('MYVAR', default=expected)
        self.assertEqual(val, expected)

    def test_will_use_env_over_default(self):
        self.set_env_var('MYVAR', 'hello')
        val = get_var('MYVAR', default='world')
        self.assertEqual(val, 'hello')

    def test_default_values_must_be_strings(self):
        self.assertRaises(EnvioParseError, get_var, 'MYVAR', default=5)
        self.assertRaises(EnvioParseError, get_var, 'MYVAR', default=5.0)
        self.assertRaises(EnvioParseError, get_var, 'MYVAR', default=True)
        self.assertRaises(EnvioParseError, get_var, 'MYVAR', default=False)
        self.assertRaises(EnvioParseError, get_var, 'MYVAR', default=[1,2])
        self.assertRaises(EnvioParseError, get_var, 'MYVAR', default={'h':'w'})

    def test_will_not_accept_missing_required_var(self):
        self.assertRaises(EnvioParseError, get_var, 'MYVAR')

    def test_can_parse_basic_coerced_values(self):
        e = EnvioParseError

        # test integer parsing
        for n in range(5):
            i = random.randrange(10000)
            self.assertEqual(get_var('MYVAR', var_type=int, default=str(i)), i)
        self.assertRaises(e, get_var, 'V', var_type=int, default='5.0')
        self.assertRaises(e, get_var, 'V', var_type=int, default='hello')
        self.assertRaises(e, get_var, 'V', var_type=int, default='1,2')
        self.assertRaises(e, get_var, 'V', var_type=int, default='true')

        # test float parsing
        for n in range(5):
            f = random.uniform(0.0, 100.0)
            self.assertEqual(get_var('MYVAR', var_type=float, default=str(f)), f)
        self.assertRaises(e, get_var, 'V', var_type=float, default='hello')
        self.assertRaises(e, get_var, 'V', var_type=float, default='1,2,3')
        self.assertRaises(e, get_var, 'V', var_type=float, default='true')

        # test truthy boolean parsing
        for n in range(len(BOOL_TRUE)):
            b = BOOL_TRUE[n]
            # create a mixed case version of the choice b
            b = ''.join([l.upper() if random.randrange(0, 2) else l for l in b])
            self.assertEqual(get_var('V', var_type=bool, default=b), True)
        self.assertRaises(e, get_var, 'V', var_type=bool, default='11')
        self.assertRaises(e, get_var, 'V', var_type=bool, default='1,1')
        self.assertRaises(e, get_var, 'V', var_type=bool, default='something')

        # test truthy
        for n in range(len(BOOL_FALSE)):
            b = BOOL_FALSE[n]
            b = ''.join([l.upper() if random.randrange(0, 2) else l for l in b])
            self.assertEqual(get_var('V', var_type=bool, default=b), False)
        self.assertRaises(e, get_var, 'V', var_type=bool, default='00')
        self.assertRaises(e, get_var, 'V', var_type=bool, default='falses,0')
        self.assertRaises(e, get_var, 'V', var_type=bool, default='sss')

    def test_can_parse_json_into_a_dict(self):
        # simple test just to prove the interface works. Otherwise we'd just be
        # testing the json.loads function
        j = '{"hello": "world", "number": 5, "f": 5.2}'
        expected = {'hello': 'world', 'number': 5, 'f': 5.2}
        self.assertEqual(get_var('MYVAR', var_type='json', default=j), expected)

    def test_can_parse_lists(self):
        # this test randomly chooses between these types and delimmitters
        types = [int, float, bool, str]
        delimmiters = [',', '|', '||', ';', '!']
        for i in range(20):
            t = random.choice(types)
            d = random.choice(delimmiters)

            if t == int:
                expected = [random.randrange(0, 100) for i in range(50)]
                input = d.join([str(x) for x in expected])

            elif t == float:
                expected = [random.uniform(0.0, 100.0) for i in range(50)]
                input = d.join([str(x) for x in expected])

            elif t == bool:
                expected = []
                input = []
                choices = BOOL_TRUE + BOOL_FALSE
                for i in range(50):
                    choice = random.choice(choices)
                    if choice in BOOL_TRUE:
                        expected.append(True)
                    else:
                        expected.append(False)
                    input.append(choice)

                input = d.join([str(x) for x in input])

            else:
                choices = ['stuff', '5', 'hello', '1', '2', '5.6', '10', 'true']
                expected = [random.choice(choices) for x in range(50)]
                input = d.join(expected)

            output = get_var('V', var_type=t, delimmiter=d, default=input, many=True)
            self.assertEqual(output, expected)
