# FairLens Initial Prototype

This repository now includes an initial executable prototype for **FairLens** focused on the first end-to-end slice described in `DELIVERY_PLAN.md`:

- offline report capture,
- pseudonymous identity generation,
- queue-based sync,
- simple disparity summary by language cohort.

## Run

```bash
python3 prototype_fairlens.py capture --locale en --exclusion-type benefits_denial --impact-level high --narrative "Denied food aid due to ID mismatch"
python3 prototype_fairlens.py capture --locale ar --exclusion-type housing_exclusion --impact-level medium --narrative "Family could not access shelter registration"
python3 prototype_fairlens.py sync
python3 prototype_fairlens.py summary
```

Data is persisted in `data/fairlens_store.json` by default.
