# Ghost Invoice

Two invoices can render identically and produce different payment proposals. Ghost Invoice is a local Python lab for investigating how invisible PDF text crosses the trust boundary between a document and a tool.

## Run the lab

Use Python 3.12. From the project folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run app.py
```

With a virtual environment active, run the CLI and tests with:

```sh
python ghost_invoice.py hidden
python -m unittest -v
```

## Try the cases

| Case | Render vs. clean | Proposed destination | Baseline | Guarded |
| --- | --- | --- | --- | --- |
| Clean | Identical | DEMO-0142 | Recorded | Recorded |
| Invisible destination override | Identical | DEMO-9099 | Recorded | Blocked |
| Visible account change | Different | DEMO-9099 | Recorded | Blocked |

Open the invisible override case, toggle **Reveal invisible text**, then click **Replay both paths**. Each replay starts with an empty in-memory ledger and receives the same proposal. The guarded path compares the proposal's invoice ID, destination, and amount in cents against a separate approval record.

The lab generates its own one-page PDFs and compares their original RGB samples at 120 DPI. The reveal handles invisible PDF text in render mode 3 in these fixtures. A deliberately vulnerable Python function simulates an agent, so this demo measures the behavior of the payment rule rather than a language model. All accounts and ledger entries are synthetic.

Start in `ghost_invoice.py` to follow generation, extraction, proposal, and authorization. `app.py` wires those functions into the demo, and `test_ghost_invoice.py` checks the expected behavior.

## Research

- [CrackedPDFs](https://arxiv.org/abs/2607.19396) studies hidden PDF prompt injection.
- [Leash](https://github.com/tusharshah21/Leash) demonstrates a poisoned invoice and payment authorization on Solana.
- [Sublime Security](https://sublime.security/blog/invoice-fraud-campaign-adds-prompt-injection-aimed-at-email-ai-agents/) documented hidden instructions in an invoice-fraud email campaign.
