# Architecture

## Layering

HTTP host -> route scripts -> core functions -> vendor API

## Rules

- Host stays dumb
- Routes stay thin
- Core owns all business logic
- Environment owns config
- Container layout must remain:
  - /service/host-python
  - /service/powershell
  - /service/src


