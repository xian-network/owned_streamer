from unittest import TestCase
from contracting.client import ContractingClient
from contracting.stdlib.bridge.time import Datetime
from pathlib import Path

class TestOwnedStreamer(TestCase):
    def setUp(self):
        self.client = ContractingClient()
        self.client.flush()
        
        # Setup test data
        self.owner = "owner"
        self.non_owner = "non_owner"
        self.stream_receiver = "receiver"
        self.test_rate = 0.1
        self.test_begins = "2024-01-01 00:00:00"
        self.test_closes = "2024-12-31 23:59:59"
        
        # Get the directory containing the test file
        current_dir = Path(__file__).parent
        
        # Navigate to contract files
        currency_fixture_path = current_dir / "fixtures" / "currency.s.py"
        owned_streamer_path = current_dir.parent / "owned_streamer.s.py"
        
        # Deploy currency contract first as it's a dependency
        with open(currency_fixture_path) as f:
            self.client.submit(f.read(), name='currency', constructor_args={'vk': self.owner})
            
        # Deploy our contract
        with open(owned_streamer_path) as f:
            self.client.submit(f.read(), name='owned_streamer', constructor_args={'initial_owner': self.owner})
            
        self.owned_streamer = self.client.get_contract('owned_streamer')
        self.currency = self.client.get_contract('currency')
        
        # Give the contract some tokens for testing
        self.currency.balances['owned_streamer'] = 100000000000000

    def test_initial_state(self):
        self.assertEqual(self.owned_streamer.get_owner(), self.owner)

    def test_renounce_ownership(self):
        # Non-owner cannot renounce
        with self.assertRaises(AssertionError):
            self.owned_streamer.renounce_ownership(signer=self.non_owner)
        
        # Owner can renounce
        self.owned_streamer.renounce_ownership(signer=self.owner)
        self.assertIsNone(self.owned_streamer.get_owner())

    def test_create_stream(self):
        # Non-owner cannot create stream
        with self.assertRaises(AssertionError):
            self.owned_streamer.create_stream(
                receiver=self.stream_receiver,
                rate=self.test_rate,
                begins=self.test_begins,
                closes=self.test_closes,
                signer=self.non_owner
            )
        
        # Owner can create stream
        stream_id = self.owned_streamer.create_stream(
            receiver=self.stream_receiver,
            rate=self.test_rate,
            begins=self.test_begins,
            closes=self.test_closes,
            signer=self.owner
        )
        
        # Verify stream was created in currency contract
        self.assertIsNotNone(stream_id)

    def test_create_stream_after_renounce(self):
        # Owner renounces ownership
        self.owned_streamer.renounce_ownership(signer=self.owner)
        
        # Previous owner cannot create stream anymore
        with self.assertRaises(AssertionError):
            self.owned_streamer.create_stream(
                receiver=self.stream_receiver,
                rate=self.test_rate,
                begins=self.test_begins,
                closes=self.test_closes,
                signer=self.owner
            )

    def test_cancel_stream(self):
        # Create a stream first
        stream_id = self.owned_streamer.create_stream(
            receiver=self.stream_receiver,
            rate=self.test_rate,
            begins=self.test_begins,
            closes=self.test_closes,
            signer=self.owner
        )
        
        # Non-owner cannot cancel stream
        with self.assertRaises(AssertionError):
            self.owned_streamer.cancel_stream(
                stream_id=stream_id,
                signer=self.non_owner
            )
        
        # Owner can cancel stream
        self.owned_streamer.cancel_stream(
            stream_id=stream_id,
            signer=self.owner
        )
        
        # Verify stream status is finalized in currency contract
        self.assertEqual(self.currency.streams[stream_id, "status"], "finalized")

    def test_return_tokens(self):
        initial_contract_balance = self.currency.balances['owned_streamer']
        initial_owner_balance = self.currency.balances[self.owner]
        return_amount = 1000

        # Non-owner cannot return tokens
        with self.assertRaises(AssertionError):
            self.owned_streamer.return_tokens(
                amount=return_amount,
                signer=self.non_owner
            )

        # Owner can return tokens
        self.owned_streamer.return_tokens(
            amount=return_amount,
            signer=self.owner
        )

        # Verify balances are updated correctly
        self.assertEqual(self.currency.balances['owned_streamer'], initial_contract_balance - return_amount)
        self.assertEqual(self.currency.balances[self.owner], initial_owner_balance + return_amount)

    def test_return_tokens_after_renounce(self):
        # Owner renounces ownership
        self.owned_streamer.renounce_ownership(signer=self.owner)
        
        # Cannot return tokens after renouncing ownership
        with self.assertRaises(AssertionError):
            self.owned_streamer.return_tokens(
                amount=1000,
                signer=self.owner
            )