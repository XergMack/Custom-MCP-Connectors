# Parity Checklist

Use this checklist before calling a new connector aligned to baseline.

## Hosting

- [ ] Same Azure hosting substrate as baseline, or variance explicitly approved
- [ ] Same ingress/public endpoint model
- [ ] Same target port behavior
- [ ] Same identity/auth pattern, or variance explicitly documented
- [ ] Same revision/rollback model

## Runtime

- [ ] Same entrypoint/startup model
- [ ] Same dependency management model
- [ ] Same container/runtime packaging model
- [ ] Same MCP transport model
- [ ] MCP runtime remains thin

## Security

- [ ] Same transport-security posture, or variance explicitly documented
- [ ] Same secret/config separation model
- [ ] Same audit/read-back expectations

## Testing Doctrine

- [ ] Test connector exposes broad read access unless technically impossible
- [ ] Test connector exposes broad write access unless technically impossible
- [ ] No arbitrary family exclusions are being used to constrain the model in test
- [ ] Any later production narrowing is explicitly documented as intentional

## Connector UI

- [ ] Name documented
- [ ] Description documented
- [ ] Auth mode documented
- [ ] Exact MCP URL documented
- [ ] Canonical MCP path documented

## Validation

- [ ] initialize passed
- [ ] 	ools/list passed
- [ ] one real 	ools/call passed
- [ ] ChatGPT connector attached successfully
- [ ] evidence files stored in repo

## Drift Control

- [ ] Any variation from baseline is documented
- [ ] Diagnostic branches are clearly labeled
- [ ] Live Azure is not being treated as the only source of truth
- [ ] Baseline repo remains the canonical reference
- [ ] Adapter-only variance rule is preserved
