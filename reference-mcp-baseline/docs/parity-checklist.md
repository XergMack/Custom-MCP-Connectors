# Parity Checklist

Use this checklist before calling a new connector aligned to baseline.

## Hosting

- [ ] Same Azure hosting substrate as baseline, or variance explicitly approved
- [ ] Same ingress/public endpoint model
- [ ] Same target port behavior
- [ ] Same identity/auth pattern, or variance explicitly documented

## Runtime

- [ ] Same entrypoint/startup model
- [ ] Same dependency management model
- [ ] Same container/runtime packaging model
- [ ] Same MCP transport model

## Security

- [ ] Same transport-security posture, or variance explicitly documented
- [ ] Same secret/config separation model
- [ ] Same write-safety posture
- [ ] Same audit/read-back expectations

## Connector UI

- [ ] Name documented
- [ ] Description documented
- [ ] Auth mode documented
- [ ] Exact MCP URL documented
- [ ] Canonical MCP path documented

## Validation

- [ ] `initialize` passed
- [ ] `tools/list` passed
- [ ] one real `tools/call` passed
- [ ] ChatGPT connector attached successfully
- [ ] evidence files stored in repo

## Drift Control

- [ ] Any variation from baseline is documented
- [ ] Diagnostic branches are clearly labeled
- [ ] Live Azure is not being treated as the only source of truth
- [ ] Baseline repo remains the canonical reference
