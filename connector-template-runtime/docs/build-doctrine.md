# Build Doctrine

## Mirror First

If a live connector already exists, mirror it into GitHub first.

## Abstract Second

Once mirrored, pull shared runtime, deploy, and validation patterns into the template runtime.

## Specialize Third

New connectors should implement only:
- target system config
- target system adapter or service logic
- tool definitions
- validation evidence

## Anti-Pattern

Do not start each connector by inventing a new runtime shell.
