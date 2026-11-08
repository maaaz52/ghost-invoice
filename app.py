"""Streamlit interface for the Ghost Invoice lab."""

from dataclasses import asdict

import streamlit as st

from ghost_invoice import APPROVAL, CASES, inspect_invoice, make_invoice, pixels_match, propose_payment, replay


st.set_page_config(page_title="Ghost Invoice", layout="wide")
st.caption("LOCAL SECURITY LAB / SYNTHETIC DATA")
st.title("Ghost Invoice")
st.markdown("Compare what a person sees with what a payment agent reads.")

case = st.radio("Case file", list(CASES), index=1, format_func=CASES.get, horizontal=True)
clean = inspect_invoice(make_invoice("clean"))
evidence = inspect_invoice(make_invoice(case))
proposal = propose_payment(evidence.text)
reveal = st.checkbox("Reveal invisible text", disabled=not evidence.invisible_lines)

original, selected = st.columns(2)
with original:
    st.subheader("Clean reference")
    st.image(clean.png, width="stretch")
with selected:
    st.subheader("Selected invoice")
    st.image(evidence.reveal_png if reveal else evidence.png, width="stretch")

same = pixels_match(clean, evidence)
st.write(f"**Original rendered pixels** · {'Identical to clean' if same else 'Different from clean'}")
st.write(f"**Invisible text spans** · {len(evidence.invisible_lines)}")
with st.expander("Inspect extracted text"):
    st.code(evidence.text, language=None)

st.subheader("Payment proposal")
st.caption("A scripted agent reads the extracted text. Each replay starts with an empty fake ledger.")
approved, proposed = st.columns(2)
with approved:
    st.markdown("**Independent approval record**")
    st.json(asdict(APPROVAL))
with proposed:
    st.markdown("**Scripted agent output**")
    st.json(asdict(proposal))

if st.button("Replay both paths", type="primary"):
    for column, label, approval in zip(st.columns(2), ("Baseline", "Guarded"), (None, APPROVAL)):
        result = replay(proposal, approval=approval)
        with column:
            st.subheader(label)
            if result.ledger:
                st.success("Recorded in the fake ledger")
            else:
                st.error("Blocked before ledger write")
            st.write(result.reason)
            st.json([asdict(payment) for payment in result.ledger])
