import unittest
from dataclasses import replace

from ghost_invoice import (
    APPROVAL, CASES, OTHER_ACCOUNT, inspect_invoice, make_invoice,
    pixels_match, propose_payment, replay,
)


class GhostInvoiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {case: inspect_invoice(make_invoice(case)) for case in CASES}

    def test_clean_proposal_passes(self):
        evidence = self.cases["clean"]
        self.assertEqual(evidence.invisible_lines, ())
        self.assertEqual(propose_payment(evidence.text), APPROVAL)
        self.assertEqual(replay(APPROVAL, approval=APPROVAL).ledger, (APPROVAL,))

    def test_hidden_override_changes_text_but_not_pixels(self):
        clean, hidden = self.cases["clean"], self.cases["hidden"]
        self.assertTrue(pixels_match(clean, hidden))
        self.assertEqual(len(hidden.invisible_lines), 1)
        self.assertIn(hidden.invisible_lines[0], hidden.text)
        self.assertNotIn(hidden.invisible_lines[0], clean.text)
        self.assertNotEqual(hidden.png, hidden.reveal_png)
        proposal = propose_payment(hidden.text)
        self.assertEqual(proposal.account, OTHER_ACCOUNT)
        self.assertEqual(replay(proposal, approval=None).ledger, (proposal,))
        self.assertEqual(replay(proposal, approval=APPROVAL).ledger, ())

    def test_visible_account_change_is_blocked_without_hidden_text(self):
        visible = self.cases["visible"]
        self.assertFalse(pixels_match(self.cases["clean"], visible))
        self.assertEqual(visible.invisible_lines, ())
        proposal = propose_payment(visible.text)
        self.assertEqual(proposal.account, OTHER_ACCOUNT)
        self.assertEqual(replay(proposal, approval=APPROVAL).ledger, ())

    def test_invoice_and_amount_mismatches_are_blocked(self):
        for proposal in (replace(APPROVAL, invoice="GI-2042"), replace(APPROVAL, amount_cents=1)):
            with self.subTest(proposal=proposal):
                self.assertEqual(replay(proposal, approval=APPROVAL).ledger, ())

    def test_missing_payment_fields_fail(self):
        with self.assertRaises(ValueError):
            propose_payment("Invoice ID: GI-1042")
