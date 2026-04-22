# Connector Template Runtime

This folder is the canonical reusable MCP connector architecture for CaberLink connectors.

## Purpose

Use this template when creating a new MCP connector so that:

- the MCP runtime shape stays consistent
- Azure Container App deployment stays consistent
- validation stays consistent
- only the target-system adapter changes

## Design Rule

The runtime shell is shared.

The only connector-specific layers should be:

- target system configuration
- target system service core / adapter logic
- tool registry entries
- handler implementations
- system-specific docs and evidence

## Derived From

This template is derived from the live SharePoint MCP baseline after parity and real bulk validation were achieved.

## Usage

1. Copy this template into a new connector folder
2. Rename connector identity values
3. Implement only the target adapter/service logic
4. Keep deploy/runtime/validation structure intact
5. Prove initialize, tools/list, and one real tools/call
