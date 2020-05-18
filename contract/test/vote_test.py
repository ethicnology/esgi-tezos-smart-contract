from os.path import dirname, join
from unittest import TestCase
from pytezos import ContractInterface, MichelsonRuntimeError


class TestContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        print("projectdir", project_dir)
        cls.test = ContractInterface.create_from(
            join(project_dir, 'src/vote.tz'))

    def test_vote_yes(self):
        user = "tz1Ud3BtcizQHv8crV6YzPHv2vvuN8zNUcB3"
        res = 1
        result = self.test.vote(
            1
        ).result(
            storage={
                "status": True,
                "yes": 0,
                "no": 0,
                "voters": set()
            },
            sender=user
        )
        self.assertEqual(res, result.storage["yes"])

    def test_vote_no(self):
        user = "tz1Ud3BtcizQHv8crV6YzPHv2vvuN8zNUcB3"
        res = 1
        result = self.test.vote(
            2
        ).result(
            storage={
                "status": True,
                "yes": 0,
                "no": 0,
                "voters": set()
            },
            sender=user
        )
        self.assertEqual(res, result.storage["no"])

    def test_vote_fail_owner(self):
        owner = "tz1QUdRxx48qhUvDkBxo3hEfvr4kzLDPKWNm"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.vote(
                1
            ).result(
                storage={
                    "status": True,
                    "yes": 0,
                    "no": 0,
                    "voters": set()
                },
                sender=owner
            )

    def test_vote_fail_disabled(self):
        user = "tz1Ud3BtcizQHv8crV6YzPHv2vvuN8zNUcB3"
        with self.assertRaises(MichelsonRuntimeError):
            self.test.vote(
                1
            ).result(
                storage={
                    "status": False,
                    "yes": 0,
                    "no": 0,
                    "voters": set()
                },
                sender=user
            )

    def test_reset_disabled(self):
        owner = "tz1QUdRxx48qhUvDkBxo3hEfvr4kzLDPKWNm"
        result = self.test.reset(1).result(
            storage={
                "status": False,
                "yes": 4,
                "no": 6,
                "voters": set()
            },
            sender=owner
        )
        self.assertEqual(0, result.storage["yes"])

    def test_reset_enabled(self):
        owner = "tz1QUdRxx48qhUvDkBxo3hEfvr4kzLDPKWNm"

        with self.assertRaises(MichelsonRuntimeError):
            self.test.reset(1).result(
                storage={
                    "status": True,
                    "yes": 0,
                    "no": 0,
                    "voters": set()
                },
                sender=owner
            )

    def test_reset_user(self):
        user = "tz1Ud3BtcizQHv8crV6YzPHv2vvuN8zNUcB3"

        with self.assertRaises(MichelsonRuntimeError):
            self.test.reset(1).result(
                storage={
                    "status": True,
                    "yes": 0,
                    "no": 0,
                    "voters": set()
                },
                sender=user
            )

    def test_pause_T2F(self):
        owner = "tz1QUdRxx48qhUvDkBxo3hEfvr4kzLDPKWNm"
        res = False
        result = self.test.pause("False").result(
            storage={
                "status": True,
                "yes": 0,
                "no": 0,
                "voters": set()
            },
            sender=owner
        )
        self.assertEqual(res, result.storage["yes"])

    def test_pause_F2T(self):
        owner = "tz1QUdRxx48qhUvDkBxo3hEfvr4kzLDPKWNm"
        res = True
        result = self.test.pause("True").result(
            storage={
                "status": False,
                "yes": 0,
                "no": 0,
                "voters": set()
            },
            sender=owner
        )
        self.assertEqual(res, result.storage["status"])

    def test_pause_user(self):
        user = "tz1Ud3BtcizQHv8crV6YzPHv2vvuN8zNUcB3"

        with self.assertRaises(MichelsonRuntimeError):
            self.test.pause("True").result(
                storage={
                    "status": False,
                    "yes": 2,
                    "no": 1,
                    "voters": set()
                },
                sender=user
            )
