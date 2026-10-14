#!/usr/bin/env python3
"""Build and check the synauson-api Python package from the protos.

    build_python.py <version> [<out dir>]   stage the package (default build/python)
    build_python.py --inspect <dist dir>    check the built wheel and sdist
    build_python.py --floors                the installed package's dependencies,
                                            the status extra's included, pinned to
                                            their lowest allowed versions
    build_python.py --check [--status]      import every module of the installed
                                            package and build both stubs; --status
                                            also reads an ErrorInfo with the extra
    build_python.py --typecheck             mypy --strict on a typed client and on
                                            the Python examples in the READMEs

Staging generates synauson/v1/*_pb2.py and *_pb2_grpc.py with grpcio-tools and
their .pyi stubs with mypy-protobuf into <out dir>/src, and writes the
pyproject.toml, README.md and license files beside it; `python -m build <out dir>`
then makes the wheel and sdist. Run it from the repository root with the
generators release.yml pins. --typecheck needs mypy, types-grpcio,
types-grpcio-status and types-protobuf, and the package installed with its
status extra.

`synauson` is a namespace package (no synauson/__init__.py), so other
distributions can add modules beside synauson.v1. They must not ship a
synauson/__init__.py either.
"""
import importlib
import pathlib
import re
import shutil
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Floors. protobuf: the gencode version the generator wrote into every _pb2.py
# (an older runtime refuses it). grpcio: the generator's version (a _pb2_grpc.py
# refuses an older grpcio). The cap: protobuf supports this gencode until at
# least 8.x; raise it once 8 is tested. The status extra: grpcio-status from the
# generator's grpc release, and the oldest googleapis-common-protos whose
# protobuf range admits the protobuf floor (1.69.2 is the first to allow 6.x).
# Re-derive the last one whenever the generator changes; --floors and the
# release's oldest-dependencies test catch a floor set that doesn't install.
COMMON_PROTOS_FLOOR = "1.69.2"

PYPROJECT = """\
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "synauson-api"
version = "{version}"
description = "Generated Python code for the synauson gRPC API"
readme = "README.md"
license = "Apache-2.0"
license-files = ["LICENSE", "NOTICE"]
requires-python = ">=3.11"
dependencies = [
    "grpcio>={grpcio}",
    "protobuf>={protobuf},<8",
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Communications :: Telephony",
    "Topic :: Multimedia :: Sound/Audio :: Speech",
    "Typing :: Typed",
]

[project.optional-dependencies]
status = [
    "grpcio-status>={grpcio}",
    "googleapis-common-protos>={common_protos}",
]

[project.urls]
Homepage = "https://synauson.com"
Source = "https://github.com/synauson/api"
Documentation = "https://github.com/synauson/api/blob/v{version}/docs/api.md"
Changelog = "https://github.com/synauson/api/blob/v{version}/CHANGELOG.md"

[tool.setuptools.packages.find]
where = ["src"]
include = ["synauson.*"]
namespaces = true

[tool.setuptools.package-data]
"*" = ["*.pyi", "py.typed"]
"""

README = """\
# synauson-api

Python code generated from the [synauson API](https://github.com/synauson/api)
protos (package `synauson.v1`), for clients of the
[Synauson](https://synauson.com) gRPC server. Python 3.11 or newer.

```sh
pip install "synauson-api[status]"
```

The `status` extra adds `grpcio-status` and `googleapis-common-protos`, which read
the `google.rpc.ErrorInfo` every error carries. The package ships type stubs for
the messages and the service stubs; the README below says how to type-check
against them.

```python
import asyncio

import grpc

from synauson.v1 import capabilities_pb2, synauson_pb2_grpc


async def main() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = synauson_pb2_grpc.SynStub(channel)
        caps = await stub.GetCapabilities(capabilities_pb2.GetCapabilitiesRequest(), timeout=10)
        print("server", caps.server_version, "API", caps.api_version)


asyncio.run(main())
```

The version is the API's: `synauson-api {version}` is tag `v{version}` of
synauson/api. The [README](https://github.com/synauson/api/blob/v{version}/README.md)
has a longer example, how to write a client and the compatibility rules, and
[docs/api.md](https://github.com/synauson/api/blob/v{version}/docs/api.md) the
reference.
"""

# Proves the stubs are typed: assert_type fails under mypy if a response is Any.
TYPED_CLIENT = """\
from typing import assert_type

import grpc
from google.rpc import error_details_pb2
from grpc_status import rpc_status

from synauson.v1 import (
    admin_pb2,
    admin_pb2_grpc,
    agent_pb2,
    capabilities_pb2,
    synauson_pb2_grpc,
)


async def run_async() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = synauson_pb2_grpc.SynStub(channel)
        caps = await stub.GetCapabilities(capabilities_pb2.GetCapabilitiesRequest(), timeout=5)
        assert_type(caps, capabilities_pb2.GetCapabilitiesResponse)
        call = stub.StreamAgentEvents(
            agent_pb2.StreamAgentEventsRequest(conference_id="c", participant_id="p")
        )
        try:
            async for event in call:
                assert_type(event, agent_pb2.AgentEvent)
        except grpc.aio.AioRpcError:
            status = await rpc_status.aio.from_call(call)
            for detail in status.details if status else []:
                info = error_details_pb2.ErrorInfo()
                if detail.Unpack(info):
                    assert_type(info.reason, str)
        finally:
            call.cancel()
        admin = admin_pb2_grpc.SynAdminStub(channel)
        snapshot = await admin.GetResourceSnapshot(
            admin_pb2.GetResourceSnapshotRequest(), timeout=5
        )
        assert_type(snapshot, admin_pb2.GetResourceSnapshotResponse)


def run_sync() -> None:
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = synauson_pb2_grpc.SynStub(channel)
        caps = stub.GetCapabilities(capabilities_pb2.GetCapabilitiesRequest(), timeout=5)
        assert_type(caps, capabilities_pb2.GetCapabilitiesResponse)
"""


def check(status):
    """Import the installed package as a client would, and build both stubs."""
    import grpc
    import synauson
    import synauson.v1

    if getattr(synauson, "__file__", None) is not None:
        sys.exit(f"synauson is a regular package ({synauson.__file__}), not a namespace")
    package = pathlib.Path(synauson.v1.__file__).parent
    modules = sorted(p.stem for p in package.glob("*_pb2*.py"))
    protos = ROOT / "synauson" / "v1"
    if protos.is_dir():
        expected = sorted(
            f"{p.stem}{suffix}" for p in protos.glob("*.proto") for suffix in ("_pb2", "_pb2_grpc")
        )
        if modules != expected:
            sys.exit(f"the package's modules {modules} don't match the protos {expected}")
    for name in modules:
        importlib.import_module(f"synauson.v1.{name}")
        if not (package / f"{name}.pyi").is_file():
            sys.exit(f"synauson/v1/{name}.pyi is missing")

    from synauson.v1 import admin_pb2_grpc, agent_pb2, synauson_pb2, synauson_pb2_grpc

    services = synauson_pb2.DESCRIPTOR.services_by_name
    assert services["Syn"].full_name == "synauson.v1.Syn"
    assert agent_pb2.AgentEvent.DESCRIPTOR.full_name == "synauson.v1.AgentEvent"
    with grpc.insecure_channel("localhost:1") as channel:
        assert hasattr(synauson_pb2_grpc.SynStub(channel), "StreamAgentEvents")
        assert hasattr(admin_pb2_grpc.SynAdminStub(channel), "ShutdownServer")
    if status:
        check_status()
    print(f"synauson-api: {len(modules)} modules import, SynStub and SynAdminStub build"
          + (", a local server's ErrorInfo reads back" if status else ""))


def check_status():
    """Fail a stream on a local server with an ErrorInfo and read it as the README does."""
    import asyncio

    import grpc
    from google.protobuf import any_pb2
    from google.rpc import code_pb2, error_details_pb2, status_pb2
    from grpc_status import rpc_status

    from synauson.v1 import agent_pb2, synauson_pb2_grpc

    class Syn(synauson_pb2_grpc.SynServicer):
        async def StreamAgentEvents(self, request, context):
            yield agent_pb2.AgentEvent(conference_id=request.conference_id, seq=1)
            detail = any_pb2.Any()
            detail.Pack(error_details_pb2.ErrorInfo(
                reason="CONFERENCE_NOT_FOUND", domain="synauson.com",
                metadata={"conferenceId": request.conference_id}))
            await context.abort_with_status(rpc_status.to_status(status_pb2.Status(
                code=code_pb2.NOT_FOUND, message="no such conference", details=[detail])))

    async def run():
        server = grpc.aio.server()
        synauson_pb2_grpc.add_SynServicer_to_server(Syn(), server)
        port = server.add_insecure_port("127.0.0.1:0")
        await server.start()
        try:
            async with grpc.aio.insecure_channel(f"127.0.0.1:{port}") as channel:
                call = synauson_pb2_grpc.SynStub(channel).StreamAgentEvents(
                    agent_pb2.StreamAgentEventsRequest(conference_id="c", participant_id="p"),
                    timeout=10,
                )
                seqs = []
                try:
                    async for event in call:
                        seqs.append(event.seq)
                except grpc.aio.AioRpcError as err:
                    assert err.code() == grpc.StatusCode.NOT_FOUND, err
                status = await rpc_status.aio.from_call(call)
                info = error_details_pb2.ErrorInfo()
                assert seqs == [1], seqs
                assert status is not None and status.details[0].Unpack(info), status
                assert (info.reason, dict(info.metadata)) == ("CONFERENCE_NOT_FOUND", {"conferenceId": "c"})
        finally:
            await server.stop(None)

    asyncio.run(run())


def typecheck():
    """mypy --strict on TYPED_CLIENT and on every Python block of both READMEs."""
    sources = {"typed_client.py": TYPED_CLIENT}
    readmes = [("package_readme", README.format(version="1.0.0"))]
    if (ROOT / "README.md").is_file():
        readmes.append(("readme", (ROOT / "README.md").read_text()))
    for name, text in readmes:
        for i, block in enumerate(re.findall(r"^```python\n(.*?)^```", text, re.M | re.S)):
            sources[f"{name}_{i}.py"] = block
    with tempfile.TemporaryDirectory() as tmp:
        for name, text in sources.items():
            (pathlib.Path(tmp) / name).write_text(text)
        # googleapis-common-protos ships .pyi files but no py.typed.
        (pathlib.Path(tmp) / "mypy.ini").write_text(
            "[mypy]\n[mypy-google.rpc.*]\nfollow_untyped_imports = True\n"
        )
        cmd = [sys.executable, "-m", "mypy", "--strict", "--no-incremental",
               "--cache-dir", str(pathlib.Path(tmp) / ".cache"), *sorted(sources)]
        print("$ mypy --strict", " ".join(sorted(sources)), flush=True)
        if subprocess.run(cmd, cwd=tmp).returncode != 0:
            sys.exit("mypy --strict failed")


def inspect(dist):
    """Check what will be uploaded: one wheel and one sdist, their files and metadata."""
    wheels, sdists = sorted(dist.glob("*.whl")), sorted(dist.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        sys.exit(f"want one wheel and one sdist in {dist}, found {wheels + sdists}")
    problems = []
    with zipfile.ZipFile(wheels[0]) as whl:
        names = whl.namelist()
        meta = next(n for n in names if n.endswith(".dist-info/METADATA"))
        metadata = whl.read(meta).decode().split("\n\n", 1)[0]
    print(wheels[0].name)
    for name in names:
        print("  ", name)
    print(metadata)
    code = [n for n in names if not n.startswith("synauson_api-")]
    if "synauson/__init__.py" in names:
        problems.append("synauson/__init__.py makes synauson a regular package")
    problems += [f"{n} is outside synauson/v1" for n in code if not n.startswith("synauson/v1/")]
    for need in ("synauson/v1/__init__.py", "synauson/v1/py.typed"):
        if need not in names:
            problems.append(f"{need} is missing")
    modules = [n for n in code if n.endswith(("_pb2.py", "_pb2_grpc.py"))]
    if not modules:
        problems.append("no generated modules")
    problems += [f"{n}i is missing" for n in modules if f"{n}i" not in names]
    for header in ("Metadata-Version: 2.4", "License-Expression: Apache-2.0",
                   "Requires-Python: >=3.11", "Provides-Extra: status"):
        if header not in metadata.splitlines():
            problems.append(f"METADATA lacks {header!r}")
    with tarfile.open(sdists[0]) as sdist:
        packed = {n.split("/", 1)[1] for n in sdist.getnames() if "/" in n}
    problems += [f"the sdist lacks {n}" for n in code if f"src/{n}" not in packed]
    if problems:
        sys.exit("\n".join(problems))
    print(f"{wheels[0].name} and {sdists[0].name}: contents and metadata as expected")


def floors():
    """name==floor for each dependency of the installed package."""
    from importlib.metadata import requires

    pins = []
    for req in requires("synauson-api"):
        name = re.match(r"[A-Za-z0-9_.-]+", req).group(0)
        floor = re.search(r">=\s*([^,;\s]+)", req)
        if floor:
            pins.append(f"{name}=={floor.group(1)}")
    print(" ".join(pins))


def main(argv):
    args = argv[1:]
    if args in (["--check"], ["--check", "--status"]):
        return check(status="--status" in args)
    if args == ["--floors"]:
        return floors()
    if args == ["--typecheck"]:
        return typecheck()
    if len(args) == 2 and args[0] == "--inspect":
        return inspect(pathlib.Path(args[1]))
    if len(args) not in (1, 2) or not re.fullmatch(r"\d+\.\d+\.\d+", args[0]):
        sys.exit(__doc__)
    stage(args[0], pathlib.Path(args[1] if len(args) == 2 else ROOT / "build" / "python"))


def stage(version, out):
    import grpc_tools
    from grpc_tools import protoc
    from importlib.metadata import version as dist_version

    if out.exists():
        shutil.rmtree(out)
    src = out / "src"
    src.mkdir(parents=True)
    protos = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "synauson" / "v1").glob("*.proto"))
    include = pathlib.Path(grpc_tools.__file__).parent / "_proto"
    scripts = sysconfig.get_path("scripts")
    plugins = {name: shutil.which(f"protoc-gen-{name}", path=scripts) for name in ("mypy", "mypy_grpc")}
    if None in plugins.values():
        sys.exit(f"mypy-protobuf's protoc plugins aren't in {scripts}: install mypy-protobuf")
    args = [
        "grpc_tools.protoc",
        f"-I{ROOT}",
        f"-I{include}",
        *(f"--plugin=protoc-gen-{name}={path}" for name, path in plugins.items()),
        f"--python_out={src}",
        f"--grpc_python_out={src}",
        f"--mypy_out={src}",
        f"--mypy_grpc_out={src}",
        *protos,
    ]
    if protoc.main(args) != 0:
        sys.exit("protoc failed")
    package = src / "synauson" / "v1"
    (package / "__init__.py").write_text('"""Generated code for the synauson.v1 API."""\n')
    (package / "py.typed").write_text("")

    (out / "pyproject.toml").write_text(
        PYPROJECT.format(
            version=version,
            grpcio=dist_version("grpcio-tools"),
            protobuf=gencode_version(package),
            common_protos=COMMON_PROTOS_FLOOR,
        )
    )
    (out / "README.md").write_text(README.format(version=version))
    for name in ("LICENSE", "NOTICE"):
        shutil.copy(ROOT / name, out / name)
    print(out)


def gencode_version(package):
    """The protobuf version the generated code was made with, its runtime floor."""
    found = set()
    for path in package.glob("*_pb2.py"):
        m = re.search(
            r"ValidateProtobufRuntimeVersion\(\s*_runtime_version\.Domain\.PUBLIC,\s*(\d+),\s*(\d+),\s*(\d+)",
            path.read_text(),
        )
        if not m:
            sys.exit(f"can't find the gencode version in {path.name}")
        found.add(".".join(m.groups()))
    if len(found) != 1:
        sys.exit(f"want one gencode version, found {sorted(found)}")
    return found.pop()


if __name__ == "__main__":
    main(sys.argv)
