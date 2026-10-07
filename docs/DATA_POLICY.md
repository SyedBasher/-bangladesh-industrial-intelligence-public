# Public-shell data policy

This repository is intentionally restricted to approved public artifacts.

## Approved content

- A high-level public product description and methodology summary.
- The self-contained `index.html` preview using **synthetic data only**.
- Public-shell tests and a limited, read-only GitHub Actions workflow.
- Explicitly reviewed public schemas or client interfaces, if approved in a later change.

## Excluded content

- Private engineering source code, SQL migrations, internal test fixtures and implementation details.
- Real DIFE/LIMA, EPB, BGMEA, BKMEA, BEPZA, DoE, BBS, DDM or corporate source extracts.
- Site coordinates, raw source downloads, PDFs, database dumps, production exports, compiled observations, internal identification graphs, client data and credentials.
- Source-specific access secrets, GitHub tokens, internal audit reports and unreleased security findings.
- Any private-repository checkout, import, artifact download or secret-bearing build step.

## Source and evidence rules

DIFE/LIMA is the establishment backbone. Organizations, reported operating units, sites, establishments, product lines and source observations are distinct concepts. Official records must not be overwritten by enrichment. Claims must retain provenance and appropriate scope in the protected evidence layer.

A company's absence from a public source is not evidence of inactivity. Data coverage is not national representativeness, estimated hazard prevalence or a composite risk measure.

## Publication gate

Every proposed public change must be reviewed for accidental real data, credentials, raw-source references and unsafe provenance disclosures. The public CI checks file paths, representative secret patterns, preview labelling and that the demo has no external network dependencies. These checks are necessary but **not sufficient**: human review is required before release.

No public files should be synchronized wholesale from the canonical development repository.
