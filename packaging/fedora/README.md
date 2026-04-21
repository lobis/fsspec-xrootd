# Fedora / EPEL 10 packaging

This directory is a starter scaffold for packaging `fsspec-xrootd` as:

- source package: `python-fsspec-xrootd`
- binary package: `python3-fsspec-xrootd`

## Current assumption

The spec currently targets the latest PyPI release, `0.5.3`, via
`%{pypi_source}`.

That is the easiest path for a Fedora review because it uses a published
upstream source archive. If you want the EPEL package to include the current
fork-only fixes from this repository, the clean next step is:

1. make a new tagged release from this fork
2. publish the sdist
3. bump `Version:` and keep using a release tarball in the spec

Using a fork snapshot is possible, but it creates more review churn than a
normal release tarball.

## Why EPEL 10 is feasible

The EPEL 10 dependency story is now good:

- `python3-fsspec` is available in EPEL 10
- `python3-xrootd` is available in EPEL 10

That means `python3-fsspec-xrootd` can satisfy Fedora/EPEL's requirement that
package dependencies be available in the official repositories.

## Expected dist-git flow

1. Submit the new package for Fedora review.
2. After approval, create or get the Fedora dist-git repo:
   `python-fsspec-xrootd`
3. Copy `python-fsspec-xrootd.spec` into the dist-git root.
4. Upload the source tarball to lookaside cache.
5. Build and iterate in Fedora.
6. Request the EPEL 10 branch:
   `fedpkg request-branch epel10 --repo python-fsspec-xrootd`
7. Build the `epel10` branch in Koji and ship via Bodhi.

## Suggested local validation

In a Fedora/EPEL packaging environment:

```bash
# Fetch sources referenced by the spec
spectool -g -R python-fsspec-xrootd.spec

# Build an SRPM
rpmbuild -bs python-fsspec-xrootd.spec

# Rebuild in mock for EPEL 10
mock -r epel-10-x86_64 --rebuild /path/to/python-fsspec-xrootd-*.src.rpm
```

## Notes on tests

The spec intentionally runs a deterministic pytest subset during `%check`.
Upstream has additional tests that start a local XRootD daemon and can be more
fragile inside constrained RPM build roots.

If mock/Koji proves reliable with the full daemon-backed test set, widening the
`%check` phase would be a good follow-up.
