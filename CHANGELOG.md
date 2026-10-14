# Changelog

Releases of the synauson API (`synauson.v1`), tagged `vX.Y.Z` in this repository and
published to PyPI as `synauson-api`. Each release names the oldest synauson server
version that serves it.

## [1.0.1] - 2026-10-14

Needs synauson server 1.8.0 or newer.

The first release on PyPI, with the same protos as 1.0.0. Version 1.0.0 is tagged
here but was never published to PyPI.

### Fixed

- Fix the API reference (`docs/api.md`), which named the package `google.protobuf`
  and printed message and enum types without links.

## [1.0.0] - 2026-10-14

Needs synauson server 1.8.0 or newer.

The first public release of the API: the `Syn` and `SynAdmin` services, their
messages, and the generated reference in `docs/api.md`. On PyPI as `synauson-api`
for Python 3.11 or newer, with type stubs; the `status` extra adds what reading
`google.rpc.ErrorInfo` needs.

A license has two pools, concurrent AI sessions and concurrent conferences.
`GetCapabilities` reports each as a `PoolUsage` (`sessions`, `conferences`), this
instance's share of each in `usage_service`, and the license's plan, always set, as
`LicensePlan` (Free, paid, developer, or unlicensed when no license is in force).
`StartConference` is refused with `CONFERENCE_POOL_LIMIT_REACHED` while the license's
conferences are in use, new work with `LICENSE_SHARE_PENDING` (`UNAVAILABLE`, retry)
while this instance holds no share of a pool yet, and new work with `LICENSE_EXPIRED`
once a developer license expires.
