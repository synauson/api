# synauson API

The Protocol Buffers definitions of the [Synauson](https://synauson.com) gRPC API.
Synauson is a media engine for voice calls with speech AI built in: you run the
server, and from your code you start conferences, connect SIP, WebRTC and file
participants, route audio between them, and get voice activity, end of turn, speech
to text and text to speech on any participant.

This repository holds only the API: the server is distributed separately. It is
published from Synauson's own repository at each API release, so it takes no pull
requests. To report a problem, open an issue in
[synauson/synauson](https://github.com/synauson/synauson/issues).

## Contents

- [What's here](#whats-here)
- [Python](#python)
- [Other languages](#other-languages)
- [Writing a client](#writing-a-client)
- [Versions and compatibility](#versions-and-compatibility)
- [License](#license)

## What's here

| Path | Contents |
|---|---|
| `synauson/v1/*.proto` | The API, package `synauson.v1`. `synauson.proto` has the `Syn` service and `admin.proto` the operator's `SynAdmin`; `errors.proto` lists every error reason; the other files hold the messages. |
| `docs/api.md` | The API reference, generated from the comments in the protos. |
| `CHANGELOG.md` | What changed in each release, and the server version it needs. |
| `buf.yaml` | A [Buf](https://buf.build) module for the protos, for linting and breaking-change checks. |

Every server also serves the standard gRPC health service, `grpc.health.v1.Health`.

## Python

Install the generated package, `synauson-api`, from PyPI. It needs Python 3.11 or
newer.

```sh
pip install "synauson-api[status]"
```

It holds the code `grpcio-tools` generates from these protos, under the `synauson.v1`
package, with type stubs for the messages and the service stubs (`SynStub`,
`SynAdminStub`), and depends on `grpcio` and `protobuf`. The `status` extra adds
`grpcio-status` and `googleapis-common-protos`, which read the `ErrorInfo` every
error carries. To type-check your code against the stubs, also install
`types-protobuf`, `types-grpcio` and `types-grpcio-status`, and set mypy's
`follow_untyped_imports` for `google.rpc.*` (googleapis-common-protos has stubs but
no `py.typed`). The package's version is the API version:
`synauson-api X.Y.Z` is tag `vX.Y.Z` here. `synauson` is a namespace package: a
package of your own under it must not have a `synauson/__init__.py`.

Start a server, then connect to it. With the container image, for example:

```sh
docker run --rm -p 50051:50051 -e SYNAUSON_LICENSE_KEY \
  cr.synauson.com/synauson/synauson-server:latest
```

This client plays a file into a conference and prints the end of each turn:

```python
import asyncio

import grpc
from google.protobuf.descriptor import EnumDescriptor
from google.rpc import error_details_pb2
from grpc_status import rpc_status

from synauson.v1 import (
    agent_pb2,
    capabilities_pb2,
    conference_pb2,
    detector_pb2,
    participant_pb2,
    synauson_pb2_grpc,
)

TIMEOUT = 10.0  # seconds, for each unary call


def enum_name(enum: EnumDescriptor, number: int) -> str:
    """A value's name, or its number when the server is newer than this client."""
    value = enum.values_by_number.get(number)
    return value.name if value else str(number)


async def error_reason(call: grpc.aio.Call) -> str:
    """The reason in a failed call's ErrorInfo, or "" when it has none."""
    status = await rpc_status.aio.from_call(call)
    for detail in status.details if status else []:
        info = error_details_pb2.ErrorInfo()
        if detail.Unpack(info):
            return info.reason
    return ""


async def main() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = synauson_pb2_grpc.SynStub(channel)

        caps = await stub.GetCapabilities(
            capabilities_pb2.GetCapabilitiesRequest(), timeout=TIMEOUT
        )
        state = enum_name(capabilities_pb2.LicenseState.DESCRIPTOR, caps.license.state)
        print("server", caps.server_version, "license", state)

        await stub.StartConference(
            conference_pb2.StartConferenceRequest(conference_id="demo"), timeout=TIMEOUT
        )
        try:
            await stub.AddFileParticipant(
                participant_pb2.AddFileParticipantRequest(
                    conference_id="demo",
                    participant_id="caller",
                    uri="file:///path/to/speech.wav",
                    detectors=detector_pb2.DetectorConfig(
                        vad=detector_pb2.VadConfig(),
                        turn_detection=detector_pb2.TurnDetectionConfig(),
                        stt=detector_pb2.SttConfig(),
                    ),
                ),
                timeout=TIMEOUT,
            )
            # A stream has no deadline: it lasts as long as the participant.
            call = stub.StreamAgentEvents(
                agent_pb2.StreamAgentEventsRequest(conference_id="demo", participant_id="caller")
            )
            try:
                async for event in call:
                    match event.WhichOneof("event"):
                        case "end_of_turn":
                            print(event.seq, "turn:", event.end_of_turn.text)
                        case "stream_ended":
                            break
                        case "subscribed" | "heartbeat":
                            pass
                        case kind:
                            # None when the server sent a case this client doesn't know.
                            print(event.seq, kind)
            except grpc.aio.AioRpcError as err:
                print("stream failed:", err.code().name, await error_reason(call))
            finally:
                call.cancel()
        finally:
            await stub.TerminateConference(
                conference_pb2.TerminateConferenceRequest(conference_id="demo"),
                timeout=TIMEOUT,
            )


asyncio.run(main())
```

With token auth on the server (`--auth=token`), send the token on every call:
`await stub.GetCapabilities(request, timeout=TIMEOUT, metadata=[("authorization", "Bearer <token>")])`.

## Other languages

Generate code from the protos with your language's gRPC plugin. Each file sets
`java_package`, `java_multiple_files`, `go_package` and `csharp_namespace`, so
`protoc` needs no extra options. For example, Java with
[protoc-gen-grpc-java](https://github.com/grpc/grpc-java):

```sh
protoc -I . --java_out=gen --grpc-java_out=gen synauson/v1/*.proto
```

This repository ships no generated Go code: `go_package` names the import path
`github.com/synauson/api/gen/go/synauson/v1` (package `synausonv1`) for code you
generate into your own module, under that path or remapped with `protoc`'s `M`
option or buf's managed mode.

## Writing a client

These hold in any language:

- **Give every unary call a deadline**, a few seconds. gRPC sets none by default, so
  a call to a stuck server waits forever. Streams take no deadline: they last as
  long as their participant or conference. Cancel a stream you stop reading.
- **Resume the agent stream yourself.** gRPC never retries a stream once it has
  started. Keep the `seq` and `stream_id` of the last event you processed, and after
  a disconnect call `StreamAgentEvents` again with them as `after_seq` and
  `stream_id`: you get exactly the events after it. The
  [reference](docs/api.md#streamagenteventsrequest) has the rules, including when to
  start afresh.
- **Detect a dead stream by its heartbeats.** The agent stream sends a heartbeat
  every `heartbeat_ms` when nothing else happens. If nothing arrives for a few
  intervals, cancel the call and resume. If you also set HTTP/2 keepalive, ping no
  more often than about once a minute: a proxy on the path may close a connection
  that pings faster.
- **Match the error reason, never the status code or the message.** Every error
  synauson returns carries a `google.rpc.ErrorInfo` in its status details, with
  domain `synauson.com`, an UPPER_SNAKE_CASE reason and string metadata;
  `ErrorReason` in `errors.proto` lists the reasons. One status code covers several
  reasons, and messages may be reworded in any release. Errors from the gRPC library
  itself (a lost connection, a deadline) carry no `ErrorInfo`: handle those, and a
  reason you don't know, by the status code.
- **Don't compress requests.** The server takes only uncompressed messages and fails
  a compressed call with UNIMPLEMENTED.
- **Ignore what you don't know** (next section): look enum names up so that a value
  you don't know gives its number instead of an error, and give a `oneof` a default
  case.

## Versions and compatibility

The proto package carries only the major version, `synauson.v1`. Releases of this
repository are tagged `v1.MINOR.PATCH`, independently of the server's version:

- A minor release adds to the API: new RPCs, messages, fields or enum values.
- A patch release changes comments and docs only.
- Within `v1`, nothing is removed or renumbered, and no field changes its type or its
  name. A field that goes is marked `deprecated` first and keeps working; removed
  numbers and names are `reserved`. A change that can't be made that way comes as a
  new package, `synauson.v2`, served beside `v1`.

Clients must ignore what they don't know: unknown fields, `oneof` cases and enum
values, and string values beyond those a field's comment lists. A newer server can
send them to an older client.

[CHANGELOG.md](CHANGELOG.md) names the oldest server version that serves each API
release, and `GetCapabilities` reports the server's own `server_version` and the API
release it implements, `api_version`. A server older than that returns `UNIMPLEMENTED` for RPCs it doesn't have
and ignores fields it doesn't know.

## License

The API definitions in this repository are licensed under the
[Apache License 2.0](LICENSE). The Synauson server is not part of this repository and
is licensed separately.
