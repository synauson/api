# synauson API reference

Package `synauson.v1`. Generated from the comments in `synauson/v1/*.proto` by
`tools/gen_api_docs.py`; edit the protos, not this file.

## Service `Syn`

The synauson media engine: conferences of participants (SIP, WebRTC, audio
files and recordings), the audio routes between them, and the voice-agent
features on each participant (voice activity, turn detection,
speech-to-text and text-to-speech).

Ids are chosen by the caller: 1 to 128 characters from `A-Z`, `a-z`,
`0-9`, `.`, `_` and `-`. Any other id fails with INVALID_ARGUMENT, reason
`INVALID_ID`. A participant id is unique within its conference.

Every error carries a `google.rpc.ErrorInfo` in the status details, with
domain "synauson.com", an UPPER_SNAKE_CASE reason and string metadata
whose keys are lowerCamelCase; `ErrorReason` lists the reasons. Match on
the reason, never on the status code or the message: the gRPC library
itself returns RESOURCE_EXHAUSTED, OUT_OF_RANGE, UNAVAILABLE and
CANCELLED without an `ErrorInfo`, and messages may be reworded in any
release.

Enums and oneofs in responses and events may gain values in later
releases: clients must accept values and cases they don't know. Requests
with an enum value the server doesn't know fail with INVALID_ARGUMENT.

Every instance also serves `SynAdmin`, for the operator, and
`grpc.health.v1.Health`.

### StartConference

`rpc StartConference(StartConferenceRequest) returns (StartConferenceResponse)`

Request: [`StartConferenceRequest`](#startconferencerequest). Response: [`StartConferenceResponse`](#startconferenceresponse).

Starts an empty conference under the caller's id. Not retry-safe: a
retry after a lost reply fails with `CONFERENCE_ALREADY_EXISTS`, which
then means the first call succeeded.

### TerminateConference

`rpc TerminateConference(TerminateConferenceRequest) returns (TerminateConferenceResponse)`

Request: [`TerminateConferenceRequest`](#terminateconferencerequest). Response: [`TerminateConferenceResponse`](#terminateconferenceresponse).

Ends a conference: removes every participant, ends every event stream
on it, and frees its resources. A retry after a lost reply fails with
`CONFERENCE_NOT_FOUND`.

### GetConference

`rpc GetConference(GetConferenceRequest) returns (GetConferenceResponse)`

Request: [`GetConferenceRequest`](#getconferencerequest). Response: [`GetConferenceResponse`](#getconferenceresponse).

Returns a conference's participants and when it started.

### GetCapabilities

`rpc GetCapabilities(GetCapabilitiesRequest) returns (GetCapabilitiesResponse)`

Request: [`GetCapabilitiesRequest`](#getcapabilitiesrequest). Response: [`GetCapabilitiesResponse`](#getcapabilitiesresponse).

Returns the server and API versions, the license, its limits and
current usage, the models' state, and this machine's speech-to-text
and text-to-speech capacity.

### AddFileParticipant

`rpc AddFileParticipant(AddFileParticipantRequest) returns (AddFileParticipantResponse)`

Request: [`AddFileParticipantRequest`](#addfileparticipantrequest). Response: [`AddFileParticipantResponse`](#addfileparticipantresponse).

Adds a participant that plays an audio file into the conference. Not
retry-safe: a retry after a lost reply fails with
`PARTICIPANT_ALREADY_EXISTS`; `GetConference` confirms the add.

### AddRecordingParticipant

`rpc AddRecordingParticipant(AddRecordingParticipantRequest) returns (AddRecordingParticipantResponse)`

Request: [`AddRecordingParticipantRequest`](#addrecordingparticipantrequest). Response: [`AddRecordingParticipantResponse`](#addrecordingparticipantresponse).

Adds a participant that records another participant's audio, and
whatever is routed to it, to a WAV file. Not retry-safe, as
`AddFileParticipant`.

### RemoveParticipant

`rpc RemoveParticipant(RemoveParticipantRequest) returns (RemoveParticipantResponse)`

Request: [`RemoveParticipantRequest`](#removeparticipantrequest). Response: [`RemoveParticipantResponse`](#removeparticipantresponse).

Removes a participant, or releases a SIP reservation. Its routes and
event streams end with it. A retry after a lost reply fails with
`PARTICIPANT_NOT_FOUND`.

### MuteParticipant

`rpc MuteParticipant(MuteParticipantRequest) returns (MuteParticipantResponse)`

Request: [`MuteParticipantRequest`](#muteparticipantrequest). Response: [`MuteParticipantResponse`](#muteparticipantresponse).

Mutes or unmutes everything a participant sends to the others.
Retry-safe: it sets the mute, so repeating it changes nothing.

### SetAudioRoutes

`rpc SetAudioRoutes(SetAudioRoutesRequest) returns (SetAudioRoutesResponse)`

Request: [`SetAudioRoutesRequest`](#setaudioroutesrequest). Response: [`SetAudioRoutesResponse`](#setaudioroutesresponse).

Replaces the conference's whole routing matrix: who hears whom.
Retry-safe: the same matrix sent again changes nothing.

### AddPriorityAudioFiles

`rpc AddPriorityAudioFiles(AddPriorityAudioFilesRequest) returns (AddPriorityAudioFilesResponse)`

Request: [`AddPriorityAudioFilesRequest`](#addpriorityaudiofilesrequest). Response: [`AddPriorityAudioFilesResponse`](#addpriorityaudiofilesresponse).

Queues audio files to play on a file participant ahead of its own
file. Not retry-safe: a retry queues the files again.

### StreamFileEvents

`rpc StreamFileEvents(StreamFileEventsRequest) returns (stream FileEvent)`

Request: [`StreamFileEventsRequest`](#streamfileeventsrequest). Response: a stream of [`FileEvent`](#fileevent).

Streams a file participant's playback events (or every file
participant's, with an empty `participant_id`), from the subscription
on.

### StreamVadEvents

`rpc StreamVadEvents(StreamVadEventsRequest) returns (stream VadEvent)`

Request: [`StreamVadEventsRequest`](#streamvadeventsrequest). Response: a stream of [`VadEvent`](#vadevent).

Streams a participant's voice activity events. Needs
`DetectorConfig.vad` on the participant.

### StreamTurnDetectionEvents

`rpc StreamTurnDetectionEvents(StreamTurnDetectionEventsRequest) returns (stream TurnDetectionEvent)`

Request: [`StreamTurnDetectionEventsRequest`](#streamturndetectioneventsrequest). Response: a stream of [`TurnDetectionEvent`](#turndetectionevent).

Streams a participant's turn detection decisions. Needs
`DetectorConfig.turn_detection` on the participant.

### StreamTranscriptEvents

`rpc StreamTranscriptEvents(StreamTranscriptEventsRequest) returns (stream TranscriptEvent)`

Request: [`StreamTranscriptEventsRequest`](#streamtranscripteventsrequest). Response: a stream of [`TranscriptEvent`](#transcriptevent).

Streams a participant's transcript. Needs `DetectorConfig.stt` on the
participant.

### StreamAgentEvents

`rpc StreamAgentEvents(StreamAgentEventsRequest) returns (stream AgentEvent)`

Request: [`StreamAgentEventsRequest`](#streamagenteventsrequest). Response: a stream of [`AgentEvent`](#agentevent).

Streams a participant's voice-agent events: speech, turns, words and
playback, in one ordered stream that can be resumed. Needs
`DetectorConfig.turn_detection` on the participant.

### ForceEndTurn

`rpc ForceEndTurn(ForceEndTurnRequest) returns (ForceEndTurnResponse)`

Request: [`ForceEndTurnRequest`](#forceendturnrequest). Response: [`ForceEndTurnResponse`](#forceendturnresponse).

Ends the participant's open turn now (reason MANUAL). Not retry-safe: a
retry may end the turn that started after the first call.

### UpdateTurnConfig

`rpc UpdateTurnConfig(UpdateTurnConfigRequest) returns (UpdateTurnConfigResponse)`

Request: [`UpdateTurnConfigRequest`](#updateturnconfigrequest). Response: [`UpdateTurnConfigResponse`](#updateturnconfigresponse).

Changes how the participant's turns end and returns the config in
effect. Retry-safe: the same update sent again changes nothing.

### Speak

`rpc Speak(SpeakRequest) returns (SpeakResponse)`

Request: [`SpeakRequest`](#speakrequest). Response: [`SpeakResponse`](#speakresponse).

Starts or continues an utterance on the participant's speaker. Needs
`DetectorConfig.tts` on the participant. Not retry-safe: a retried
Speak whose first call reached the speaker speaks its text twice.

### CancelUtterance

`rpc CancelUtterance(CancelUtteranceRequest) returns (CancelUtteranceResponse)`

Request: [`CancelUtteranceRequest`](#cancelutterancerequest). Response: [`CancelUtteranceResponse`](#cancelutteranceresponse).

Stops an utterance (or every interruptible one) now. Retry-safe: an
utterance already stopped is not stopped again.

### AddSipParticipant

`rpc AddSipParticipant(AddSipParticipantRequest) returns (AddSipParticipantResponse)`

Request: [`AddSipParticipantRequest`](#addsipparticipantrequest). Response: [`AddSipParticipantResponse`](#addsipparticipantresponse).

Adds a SIP call's media as a participant, once both sides' media are
known. Synauson handles RTP only; the caller does the SIP signalling.
Not retry-safe, as `AddFileParticipant`.

### SendDtmf

`rpc SendDtmf(SendDtmfRequest) returns (SendDtmfResponse)`

Request: [`SendDtmfRequest`](#senddtmfrequest). Response: [`SendDtmfResponse`](#senddtmfresponse).

Sends a DTMF digit to a SIP participant's peer. Not retry-safe: a retry
sends the digit again.

### StreamDtmfEvents

`rpc StreamDtmfEvents(StreamDtmfEventsRequest) returns (stream DtmfEvent)`

Request: [`StreamDtmfEventsRequest`](#streamdtmfeventsrequest). Response: a stream of [`DtmfEvent`](#dtmfevent).

Streams the DTMF digits a SIP participant's peer sends, from the
subscription on.

### GetSipStats

`rpc GetSipStats(GetSipStatsRequest) returns (GetSipStatsResponse)`

Request: [`GetSipStatsRequest`](#getsipstatsrequest). Response: [`GetSipStatsResponse`](#getsipstatsresponse).

Returns a SIP participant's RTP receive statistics.

### ReserveSipParticipant

`rpc ReserveSipParticipant(ReserveSipParticipantRequest) returns (ReserveSipParticipantResponse)`

Request: [`ReserveSipParticipantRequest`](#reservesipparticipantrequest). Response: [`ReserveSipParticipantResponse`](#reservesipparticipantresponse).

Reserves the local ports for an outbound call's SDP offer, the first
step of a two-phase add; `ConnectSipParticipant` is the second. Not
retry-safe: a retry fails with `PARTICIPANT_ALREADY_EXISTS`.

### ConnectSipParticipant

`rpc ConnectSipParticipant(ConnectSipParticipantRequest) returns (ConnectSipParticipantResponse)`

Request: [`ConnectSipParticipantRequest`](#connectsipparticipantrequest). Response: [`ConnectSipParticipantResponse`](#connectsipparticipantresponse).

Starts a participant reserved by `ReserveSipParticipant`, with the
media the peer's SDP answer negotiated. Not retry-safe: a retry fails
with `PARTICIPANT_ALREADY_EXISTS`.

### AddWebRtcParticipant

`rpc AddWebRtcParticipant(AddWebRtcParticipantRequest) returns (AddWebRtcParticipantResponse)`

Request: [`AddWebRtcParticipantRequest`](#addwebrtcparticipantrequest). Response: [`AddWebRtcParticipantResponse`](#addwebrtcparticipantresponse).

Adds a WebRTC peer (a browser, say) as a participant: sends its SDP
offer, returns synauson's answer. Not retry-safe: a retry fails with
`PARTICIPANT_ALREADY_EXISTS` and the answer is lost, so remove the
participant and add it again.

### AddWebRtcIceCandidate

`rpc AddWebRtcIceCandidate(AddWebRtcIceCandidateRequest) returns (AddWebRtcIceCandidateResponse)`

Request: [`AddWebRtcIceCandidateRequest`](#addwebrtcicecandidaterequest). Response: [`AddWebRtcIceCandidateResponse`](#addwebrtcicecandidateresponse).

Passes one of the peer's ICE candidates to synauson (trickle ICE).
Retry-safe: a candidate added twice is used once.

### StreamWebRtcIceCandidates

`rpc StreamWebRtcIceCandidates(StreamWebRtcIceCandidatesRequest) returns (stream WebRtcIceCandidate)`

Request: [`StreamWebRtcIceCandidatesRequest`](#streamwebrtcicecandidatesrequest). Response: a stream of [`WebRtcIceCandidate`](#webrtcicecandidate).

Streams synauson's own ICE candidates for the peer: those found before
the subscription, then new ones as they are found.

### GetWebRtcStats

`rpc GetWebRtcStats(GetWebRtcStatsRequest) returns (GetWebRtcStatsResponse)`

Request: [`GetWebRtcStatsRequest`](#getwebrtcstatsrequest). Response: [`GetWebRtcStatsResponse`](#getwebrtcstatsresponse).

Returns a WebRTC participant's connection state and the options it
runs with.

## Service `SynAdmin`

Operating the server: what it uses, and stopping it. Served on the same
address and behind the same authentication as `Syn`; give these calls
to the operator's tools, not to agents. Errors carry an `ErrorInfo`, as
`Syn` describes.

### ShutdownServer

`rpc ShutdownServer(ShutdownServerRequest) returns (ShutdownServerResponse)`

Request: [`ShutdownServerRequest`](#shutdownserverrequest). Response: [`ShutdownServerResponse`](#shutdownserverresponse).

Terminates every conference, then stops the server. Returns at once;
the drain runs in the background. From the call on, health reports
NOT_SERVING and new conferences fail with `SERVER_SHUTTING_DOWN`.
Retry-safe: a second call while the drain runs changes nothing.

### GetResourceSnapshot

`rpc GetResourceSnapshot(GetResourceSnapshotRequest) returns (GetResourceSnapshotResponse)`

Request: [`GetResourceSnapshotRequest`](#getresourcesnapshotrequest). Response: [`GetResourceSnapshotResponse`](#getresourcesnapshotresponse).

Returns the server's memory, threads and conferences now, for
monitoring.

## synauson/v1/admin.proto

### ShutdownServerRequest

Stop the server.

| Field | Number | Type | Description |
|---|---|---|---|
| `grace_period_seconds` | 1 | `int32` | How long to wait for the conferences to terminate before the server stops anyway, in seconds; at least 1 (smaller values count as 1). |

### ShutdownServerResponse

The shutdown started; the server stops serving once it completes.

### GetResourceSnapshotRequest

Ask for a resource snapshot.

### GetResourceSnapshotResponse

A resource snapshot.

| Field | Number | Type | Description |
|---|---|---|---|
| `snapshot` | 1 | [`ResourceSnapshot`](#resourcesnapshot) | What the server uses now. |

### ResourceSnapshot

What the server uses at one moment.

| Field | Number | Type | Description |
|---|---|---|---|
| `capture_time` | 1 | `google.protobuf.Timestamp` | When it was taken. |
| `process_memory` | 2 | [`ProcessMemory`](#processmemory) | The server process's memory and threads. |
| `runtime_stats` | 3 | [`RuntimeStats`](#runtimestats) | The server's own thread pools. |
| `cgroup_memory` | 4 | [`CgroupMemory`](#cgroupmemory) | The memory limit and usage of the control group the server runs in. |
| `conferences` | 5 | repeated [`ConferenceInfo`](#conferenceinfo) | Each running conference, in no particular order; at most the operator's conference cap, when one is set. |

### ProcessMemory

The server process's memory and threads, where the platform reports
them (Linux); on other platforms both fields are unset.

| Field | Number | Type | Description |
|---|---|---|---|
| `vmrss_bytes` | 1 | optional `int64` | Resident memory (VmRSS), in bytes. |
| `threads` | 2 | optional `int32` | Threads in the process. |

### RuntimeStats

The server's own thread pools.

| Field | Number | Type | Description |
|---|---|---|---|
| `worker_threads` | 1 | `int32` | Threads that run the server's request handling and conference tasks. |
| `blocking_threads` | 2 | `int32` | Threads in the pool for blocking work, which grows and shrinks on demand. |

### CgroupMemory

The memory limit and usage of the server's control group (Linux).

| Field | Number | Type | Description |
|---|---|---|---|
| `limit_bytes` | 1 | optional `int64` | The smallest memory limit on the control group or any ancestor, in bytes; absent when there is none. |
| `used_bytes` | 2 | optional `int64` | Memory the control group uses now, in bytes; absent when unreadable. |
| `version` | 3 | [`CgroupVersion`](#cgroupversion) | The interface read. May gain values: accept ones you don't know. |

### ConferenceInfo

One running conference.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | The conference's id. |
| `participant_count` | 2 | `int32` | How many participants it has. |

### CgroupVersion

Which control group interface the server read its memory from.

| Value | Number | Description |
|---|---|---|
| `CGROUP_VERSION_UNSPECIFIED` | 0 | Not set; never sent. |
| `CGROUP_VERSION_V2` | 1 | Control groups v2 (the unified hierarchy). |
| `CGROUP_VERSION_V1` | 2 | Control groups v1. |
| `CGROUP_VERSION_NONE` | 3 | Neither is readable, or the platform has no control groups; the memory fields are absent. |

## synauson/v1/agent.proto

### StreamAgentEventsRequest

Subscribe to a participant's voice-agent events.

The stream keeps its last 512 events. Without after_seq a subscription
gets every kept event, then live ones. To resume after a disconnect, send
the last seq you processed as after_seq with its stream_id: you get
exactly the events after it, none twice.

Each subscriber has its own queue of 256 events and never slows the
conference. One that falls that far behind gets the events already
queued, then the stream ends with `AGENT_SUBSCRIBER_LAGGED` (metadata
`lastSeq`); resume from that seq while it is still kept.

The stream ends normally after `AgentStreamEnded`, when the participant
is removed or its conference terminated; a server shutdown terminates
every conference first. Any other end (a lost connection, a lagging
subscriber, the server stopping without a drain) can be resumed with the
cursor. Without events the stream sends an `AgentHeartbeat` every
`heartbeat_ms`: a client that gets nothing for a few intervals should
treat the stream as dead, cancel it and resume.

Errors: `INVALID_ID`; `INVALID_ARGUMENT` (an `after_seq` past the newest
seq); `CONFERENCE_NOT_FOUND`; `PARTICIPANT_NOT_FOUND`;
`TURN_DETECTION_REQUIRED`; `AGENT_STREAM_MISMATCH` (metadata `streamId`,
the current one); `AGENT_REPLAY_EXPIRED` (metadata `oldestSeq`,
`lastSeq`, `streamId`).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant whose events to stream. |
| `after_seq` | 3 | optional `int64` | Resume: send the events after this seq. Unset sends every event the stream still keeps, then live ones. A cursor older than the oldest kept event fails with `AGENT_REPLAY_EXPIRED`: subscribe again without one. |
| `stream_id` | 4 | optional `int64` | The stream `after_seq` came from (`AgentEvent.stream_id`). When set it must be the participant's current stream, else `AGENT_STREAM_MISMATCH`: the participant was added again, so start on the new stream. |
| `heartbeat_ms` | 5 | optional `int32` | Heartbeat interval in ms (a duration): an `AgentHeartbeat` comes whenever nothing else did for this long. 1000 when unset; clamped to 100 to 30000. |

### AgentEvent

One event. Every subscriber gets the events in the same order. Field
numbers of the oneof group its cases: 10-19 stream control, 20-39 speech
and turns, 40-59 playback.

The events that end a turn (`AgentEndOfTurn`) and an utterance
(`AgentUtteranceDone`, `AgentUtteranceInterrupted`,
`AgentUtteranceFailed`) are closed sets in v1: a later release adds no
other way for a turn or an utterance to end, so a client can track open
turns and utterances by them. Other cases may be added.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | The participant's conference. |
| `participant_id` | 2 | `string` | The participant the event is about. |
| `stream_id` | 3 | `int64` | Names the participant's stream. A participant added again under the same id gets a new `stream_id`, and its seqs start again from 1. |
| `seq` | 4 | `int64` | Strictly increasing from 1 over stored events. `AgentSubscribed` and `AgentHeartbeat` aren't stored: they repeat the last seq this subscription has (the cursor, for `AgentSubscribed`). |
| `event_time` | 5 | `google.protobuf.Timestamp` | Wall-clock time the event was made. |
| `subscribed` | 10 | oneof event: [`AgentSubscribed`](#agentsubscribed) | First on every subscription. |
| `heartbeat` | 11 | oneof event: [`AgentHeartbeat`](#agentheartbeat) | Nothing else happened for the heartbeat interval. |
| `error` | 12 | oneof event: [`AgentError`](#agenterror) | A recoverable problem; the stream goes on. |
| `stream_ended` | 13 | oneof event: [`AgentStreamEnded`](#agentstreamended) | Last on the stream. |
| `speech_started` | 20 | oneof event: [`AgentSpeechStarted`](#agentspeechstarted) | Voice activity detection heard speech start. |
| `speech_stopped` | 21 | oneof event: [`AgentSpeechStopped`](#agentspeechstopped) | Voice activity detection heard the speech stop. |
| `turn_started` | 22 | oneof event: [`AgentTurnStarted`](#agentturnstarted) | A turn started. |
| `turn_words` | 23 | oneof event: [`AgentTurnWords`](#agentturnwords) | More of the open turn's words. |
| `eager_end_of_turn` | 24 | oneof event: [`AgentEagerEndOfTurn`](#agenteagerendofturn) | The open turn may have ended at a pause. |
| `turn_resumed` | 25 | oneof event: [`AgentTurnResumed`](#agentturnresumed) | The turn's last eager end of turn was premature. |
| `end_of_turn` | 26 | oneof event: [`AgentEndOfTurn`](#agentendofturn) | A turn ended. |
| `turn_config_updated` | 27 | oneof event: [`AgentTurnConfigUpdated`](#agentturnconfigupdated) | UpdateTurnConfig changed the turn config. |
| `utterance_started` | 40 | oneof event: [`AgentUtteranceStarted`](#agentutterancestarted) | An utterance's first sample played. |
| `words_played` | 41 | oneof event: [`AgentWordsPlayed`](#agentwordsplayed) | More of an utterance's words fully played. |
| `utterance_done` | 42 | oneof event: [`AgentUtteranceDone`](#agentutterancedone) | An utterance played to its end. |
| `utterance_interrupted` | 43 | oneof event: [`AgentUtteranceInterrupted`](#agentutteranceinterrupted) | An utterance stopped before its end. |
| `utterance_failed` | 44 | oneof event: [`AgentUtteranceFailed`](#agentutterancefailed) | An utterance failed. |

`oneof event`: What happened. Clients must ignore cases they don't know.

### AgentSubscribed

First on every subscription.

| Field | Number | Type | Description |
|---|---|---|---|
| `oldest_seq` | 1 | `int64` | The oldest event the stream still keeps, 0 when it keeps none. |
| `last_seq` | 2 | `int64` | The stream's newest seq when the subscription started, 0 before its first event. |
| `stt` | 3 | `bool` | Whether speech-to-text runs on the participant. |
| `turn_config` | 4 | [`TurnConfig`](#turnconfig) | The turn config in effect. |
| `tts` | 5 | `bool` | Whether the participant has a speaker (text-to-speech). |
| `voice` | 6 | optional `string` | The speaker's default voice, when it has one. |

### AgentHeartbeat

Sent when nothing else was for the heartbeat interval.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_ms` | 1 | `int64` | The conference's time now. |
| `stt_decoded_ms` | 2 | optional `int64` | The conference time speech-to-text has transcribed up to, when it runs and has reported. |
| `stt_backlog_ms` | 3 | optional `int64` | Audio waiting to be transcribed (a duration), when speech-to-text reported it. |

### AgentError

A recoverable problem: the stream goes on. Stream-fatal errors end the
RPC with a status carrying a `google.rpc.ErrorInfo` instead.

| Field | Number | Type | Description |
|---|---|---|---|
| `reason` | 1 | `string` | Stable, UPPER_SNAKE_CASE, one of `ErrorReason`'s `AgentError` values; others may be added:<br><br>`TURN_DETECTION_FAILED`: turn detection stopped on the participant; turns end only by timeout or `ForceEndTurn` from then on.<br><br>`TURN_DECISION_MISSING`: a speech end got no turn detection decision within 2 s; the timeout still ends the turn.<br><br>`STT_STOPPED`: speech-to-text failed; turns end with the words they had, and later ones without words.<br><br>`STT_LAGGING`: the transcription's backlog passed the participant's `SttConfig.turn_drain_ms` (at least 500 ms; metadata `backlogMs`, `thresholdMs`). Turns may end incomplete, their late words opening the next turn or a late turn of their own. Sent again only after the backlog falls to half the threshold. |
| `message` | 2 | `string` | What happened, for people. Don't match on it. |
| `metadata` | 3 | map<`string`, `string`> | Details, keyed by lowerCamelCase name; which keys come depends on the reason. |
| `turn_id` | 4 | optional `int64` | The turn it concerns, if any. |

### AgentStreamEnded

Last on the stream; the RPC then completes.

| Field | Number | Type | Description |
|---|---|---|---|
| `reason` | 1 | [`AgentStreamEndReason`](#agentstreamendreason) | Why the stream ended. |

### AgentSpeechStarted

Voice activity detection heard speech start. This is raw voice activity:
noise can start it too. It carries no turn and goes out at once.

| Field | Number | Type | Description |
|---|---|---|---|
| `at_ms` | 1 | `int64` | Where the speech started, before the detector's debounce, so it precedes the event by up to VadConfig.min_speech_ms. |
| `probability` | 2 | `float` | The detector's probability for the window that confirmed it. |

### AgentSpeechStopped

Voice activity detection heard the speech stop. It carries no turn and
goes out at once.

| Field | Number | Type | Description |
|---|---|---|---|
| `at_ms` | 1 | `int64` | Where the speech stopped, before the detector's debounce, so it precedes the event by up to VadConfig.min_silence_ms. |
| `speech_ms` | 2 | `int64` | How long it lasted (a duration): at_ms less its AgentSpeechStarted's. |

### AgentTurnStarted

A turn started. Turn ids rise by one from 1. Each AgentTurnStarted is
followed by exactly one AgentEndOfTurn for it, and no event of a turn
(its start, its words, its errors) comes before the previous turn's
AgentEndOfTurn. Speech after a pause stays in the open turn unless turn
detection then calls the pause the turn's end.

A late turn holds words speech-to-text committed after the turn before it
ended incomplete (it lagged past SttConfig.turn_drain_ms) when the
participant said nothing more. It comes once the words are transcribed,
with no speech of its own; if speech starts first, the words open that
speech's turn instead.

| Field | Number | Type | Description |
|---|---|---|---|
| `turn_id` | 1 | `int64` | The turn's id. |
| `start_ms` | 2 | `int64` | Where the turn's speech started (the voice activity detector's speech start); for a late turn, its first word's start. |
| `word_backed` | 3 | `bool` | Whether words started it. True when speech-to-text runs: the turn starts with its first word, and a turn without words is never sent. False without speech-to-text, where the speech start starts it. |

### AgentTurnWords

More of the open turn's words, each once it is complete (the next word
started, or the turn closed). A turn's AgentTurnWords, in order, are
exactly its AgentEndOfTurn's words.

| Field | Number | Type | Description |
|---|---|---|---|
| `turn_id` | 1 | `int64` | The open turn's id. |
| `words` | 2 | repeated [`Word`](#word) | The words, in order. |
| `stt_backlog_ms` | 3 | optional `int64` | Audio waiting to be transcribed (a duration), when speech-to-text reported it. |

### Word

One transcribed word. Its times are when the model emitted it, which
trails the audio by up to the model's commit delay (about 800 ms for the
default model before a pause, less in running speech).

| Field | Number | Type | Description |
|---|---|---|---|
| `text` | 1 | `string` | The word with its punctuation, no leading space ("Hello,"). A turn's first word leaves out the end of the sentence before it. |
| `start_ms` | 2 | `int64` | When its first piece was emitted. |
| `end_ms` | 3 | `int64` | Where its last piece ends. |
| `confidence` | 4 | optional `float` | The model's lowest confidence in its pieces, in [0, 1]; unset when the model gives none for a piece. A relative score (a low one flags a word worth confirming), not a calibrated probability of being right. |

### AgentEagerEndOfTurn

The open turn may have ended: a pause turn detection hasn't confirmed as
its end (TurnConfig.eager), so an agent can start preparing its reply.
Its text is what the turn's AgentEndOfTurn will say if this pause ends
it: an AgentEndOfTurn's text is the last AgentEagerEndOfTurn's unless an
AgentTurnResumed came between them. A turn may have several, each after
an AgentTurnResumed.

With speech-to-text, synauson forecasts the pause's last words ahead of
real time. If turn detection ends the turn before the forecast is ready,
no eager end is sent for that pause: the AgentEndOfTurn comes as soon as
it would have.

| Field | Number | Type | Description |
|---|---|---|---|
| `turn_id` | 1 | `int64` | The open turn's id. |
| `text` | 2 | `string` | Its words joined by single spaces; empty without speech-to-text. |
| `words` | 3 | repeated [`Word`](#word) | The turn's words up to the pause: those sent in AgentTurnWords so far, then the rest, which may include words forecast but not yet committed. Empty without speech-to-text. |
| `speech_end_ms` | 4 | `int64` | Where the pause's speech ended (the voice activity detector's speech end). |
| `probability` | 5 | optional `float` | Turn detection's probability for the pause, when the eager end came on its decision; unset when it came at the speech end (eager_threshold 0). |
| `latency` | 6 | [`TurnLatency`](#turnlatency) | How long it took; drain_ms is how long speech-to-text took for the text, from the pause becoming eager. |

### AgentTurnResumed

The turn's last AgentEagerEndOfTurn was premature: the turn goes on, and
its text no longer stands. At most one per AgentEagerEndOfTurn.

| Field | Number | Type | Description |
|---|---|---|---|
| `turn_id` | 1 | `int64` | The open turn's id. |
| `cause` | 2 | [`TurnResumeCause`](#turnresumecause) | What took the eager end back. |
| `at_ms` | 3 | `int64` | SPEECH: where it restarted (the voice activity detector's speech start). WORDS: when the first word that differs was emitted, or when the turn ended if its AgentEndOfTurn is what differs. |

### AgentEndOfTurn

A turn ended: exactly one per AgentTurnStarted, in turn order. With
speech-to-text it waits for the turn's transcript; a turn it finds no
words in is not on this stream at all. Without speech-to-text it comes at
once. A late turn ends for the reason, and with the probability, of the
turn before it (STREAM_ENDED when there was none).

| Field | Number | Type | Description |
|---|---|---|---|
| `turn_id` | 1 | `int64` | The turn's id. |
| `reason` | 2 | [`TurnEndReason`](#turnendreason) | Why it ended. |
| `text` | 3 | `string` | Its words joined by single spaces: the turn's TurnTranscript text without its leading space when speech-to-text runs; empty otherwise. |
| `words` | 4 | repeated [`Word`](#word) | The turn's words, in order; empty without speech-to-text. |
| `start_ms` | 5 | `int64` | Where the turn's speech started, as in its AgentTurnStarted. |
| `speech_end_ms` | 6 | `int64` | Where the turn's speech ended: the voice activity detector's last speech end, or when the turn ended if the participant was still speaking; a late turn's last word's end. |
| `probability` | 7 | optional `float` | Turn detection's probability for the turn's last pause, when it decided. |
| `complete` | 8 | `bool` | False when the text may lack the turn's last words: speech-to-text ran out of drain time, or stopped, first. |
| `latency` | 9 | [`TurnLatency`](#turnlatency) | How long the end of turn took. |

### TurnLatency

How long an end of turn took. Every field is a duration.

| Field | Number | Type | Description |
|---|---|---|---|
| `since_speech_end_ms` | 1 | optional `int64` | From the speech end to the event. |
| `decision_ms` | 2 | optional `int64` | Turn detection's decision: its time queued plus its inference (reason MODEL only). |
| `drain_ms` | 3 | optional `int64` | From the turn's end to speech-to-text settling its text. |
| `stt_backlog_ms` | 4 | optional `int64` | Audio waiting to be transcribed when the turn ended. |

### TurnConfig

How a participant's turns end; every field set.

| Field | Number | Type | Description |
|---|---|---|---|
| `end_of_turn_threshold` | 1 | `float` | Turn detection's probability at or above which a pause ends the turn. |
| `eager` | 2 | `bool` | Eager end of turn: an AgentEagerEndOfTurn for each pause that may end the turn. With speech-to-text it needs the instance to allow it (SttCapacityInfo.eager), else it is refused. |
| `eager_threshold` | 3 | `float` | Turn detection's probability at or above which a pause sends the eager end of turn; 0 (the default) sends it at the speech end. At most `end_of_turn_threshold`. |
| `end_of_turn_timeout_ms` | 4 | `int32` | Silence after a speech end that ends the turn anyway (reason TIMEOUT), in ms (a duration); 0 turns it off. Default 5000. |

### TurnConfigUpdate

Changes to a `TurnConfig`: each field set replaces the current one; an
unset field keeps it. A value out of range is refused
(`INVALID_TURN_CONFIG`) and leaves the config unchanged.

| Field | Number | Type | Description |
|---|---|---|---|
| `end_of_turn_threshold` | 1 | optional `float` | In [0, 1]. |
| `eager` | 2 | optional `bool` | Turning it on with speech-to-text is refused unless the instance allows it (`SttCapacityInfo.eager`). |
| `eager_threshold` | 3 | optional `float` | In [0, 1], and at most `end_of_turn_threshold`. |
| `end_of_turn_timeout_ms` | 4 | optional `int32` | 0 to 60000 ms (a duration). A changed timeout applies to the open turn's current pause too. |

### AgentTurnConfigUpdated

UpdateTurnConfig changed the turn config.

| Field | Number | Type | Description |
|---|---|---|---|
| `config` | 1 | [`TurnConfig`](#turnconfig) | The config now in effect. |

### ForceEndTurnRequest

End the participant's open turn now. Its AgentEndOfTurn (reason MANUAL)
follows on the stream: at once without speech-to-text; with it once the
transcript settles, which synauson speeds up by forecasting the turn's
last words (at most SttConfig.turn_drain_ms). If the participant is still
speaking, the speech ends where the turn did and the next turn starts at
once.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND`,
`TURN_DETECTION_REQUIRED`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant whose turn to end. |

### ForceEndTurnResponse

What ForceEndTurn ended.

| Field | Number | Type | Description |
|---|---|---|---|
| `ended` | 1 | `bool` | Whether a turn was open and is ending; its AgentEndOfTurn (reason MANUAL) follows on the stream. |
| `turn_id` | 2 | optional `int64` | The turn's id, when it is on the stream. With speech-to-text a turn is on the stream once it has a word: one ended before its first has no id here, and is sent, with its AgentEndOfTurn, only if speech-to-text finds words in it. |

### UpdateTurnConfigRequest

Change how the participant's turns end.

Errors: `INVALID_ID`, `INVALID_TURN_CONFIG` (a value out of range; the
config is unchanged), `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND`,
`TURN_DETECTION_REQUIRED`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant whose turn config to change. |
| `update` | 3 | [`TurnConfigUpdate`](#turnconfigupdate) | The changes; unset changes nothing. |

### UpdateTurnConfigResponse

The turn config after UpdateTurnConfig.

| Field | Number | Type | Description |
|---|---|---|---|
| `config` | 1 | [`TurnConfig`](#turnconfig) | The config now in effect. |
| `seq` | 2 | `int64` | The seq of the `AgentTurnConfigUpdated` event that announced it. |

### SpeakRequest

Speak: start or continue an utterance on the participant's speaker. The
reply comes once the speaker has the text, never after synthesis, and a
Speak may come while earlier utterances still play (they queue). Speech
starts after a short first chunk, then synthesis runs ahead of playback.

Speak is not retry-safe: a Speak whose reply was lost may have reached
the speaker, and sending it again speaks its text twice. After a lost
reply, cancel the utterance or carry on with the next text.

Errors: `INVALID_ID`; `INVALID_SPEAK` (text over its cap, voice or speed
after the first Speak, an unknown voice, a speed out of range, more than
64 utterances queued); `CONFERENCE_NOT_FOUND`; `PARTICIPANT_NOT_FOUND`;
`TTS_REQUIRED` (no speaker); `UTTERANCE_ENDED` (the utterance was ended,
finished, was interrupted or failed).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant whose speaker speaks. |
| `utterance_id` | 3 | `string` | Required. Chosen by the caller, an id as `Syn` describes; every playback event echoes it. A new id starts an utterance; a used one continues it until it ends. |
| `text` | 4 | `string` | More of the utterance's text, as written: the speaker normalizes it, so numbers, money, dates and codes are read as a person would. At most 16 KiB of UTF-8 per Speak, 64 KiB per utterance. |
| `release` | 5 | [`SpeakRelease`](#speakrelease) | What this text ends; unset is `SPEAK_RELEASE_NONE`. |
| `interruptible` | 6 | optional `bool` | Only on an utterance's first Speak. Whether CancelUtterance may stop it (default true). |
| `preemptible` | 7 | optional `bool` | Only on an utterance's first Speak. Whether the next new utterance stops it, reason PREEMPTED (default false). |
| `voice` | 8 | optional `string` | Only on an utterance's first Speak: a voice instead of the speaker's default (TtsConfig.voice). |
| `speed` | 9 | optional `float` | Only on an utterance's first Speak: speaking rate, 0.25 to 4 (1 is the voice's own). |

### SpeakResponse

The speaker has the text.

| Field | Number | Type | Description |
|---|---|---|---|
| `utterance_id` | 1 | `string` | The utterance's id, as sent. |
| `created` | 2 | `bool` | Whether this Speak started the utterance. |

### CancelUtteranceRequest

Stop an utterance's audio now and drop its queue. The audio stops within
one 20 ms buffer of the command reaching the conference, plus what the
participant's mixer already holds (20 ms on SIP, 60 ms on WebRTC); the
rest of the call's audio is untouched.

Errors: `INVALID_ID`; `CONFERENCE_NOT_FOUND`; `PARTICIPANT_NOT_FOUND`;
`UNKNOWN_UTTERANCE` (an id the speaker never had); `TTS_REQUIRED`;
`UTTERANCE_NOT_INTERRUPTIBLE` (spoken with `interruptible` false).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant whose speaker to stop. |
| `utterance_id` | 3 | optional `string` | Unset cancels every interruptible utterance, playing or queued. |

### CancelUtteranceResponse

What CancelUtterance stopped. Each canceled utterance's
AgentUtteranceInterrupted is on the stream before this response.

| Field | Number | Type | Description |
|---|---|---|---|
| `cancelled` | 1 | repeated [`CancelledUtterance`](#cancelledutterance) | Each utterance canceled, in order. Empty when the utterance had already finished, or none was speaking. |

### CancelledUtterance

One utterance CancelUtterance stopped.

| Field | Number | Type | Description |
|---|---|---|---|
| `utterance_id` | 1 | `string` | The utterance's id. |
| `heard_text` | 2 | `string` | What the caller heard: the text up to its last fully played word. |
| `heard_ms` | 3 | `int64` | How much of its audio played (a duration). |
| `seq` | 4 | `int64` | The seq of its AgentUtteranceInterrupted on the agent stream. |

### AgentUtteranceStarted

The first sample of an utterance played. Exactly one per utterance that
plays any audio, before its AgentWordsPlayed; then exactly one of
AgentUtteranceDone, AgentUtteranceInterrupted or AgentUtteranceFailed.
Utterances play one after another in the order they were started, so the
events of utterances that play never interleave, but one that fails
before it plays is reported when it fails: match events by utterance_id.

"Played" means the audio passed the speaker's clock-synced point, the
last place synauson can still stop it; the audio leaves synauson about
egress_delay_ms later.

| Field | Number | Type | Description |
|---|---|---|---|
| `utterance_id` | 1 | `string` | The utterance's id. |
| `at_ms` | 2 | `int64` | When its first sample passed the speaker's clock-synced point, the last place synauson can still stop it. |
| `time_to_first_audio_ms` | 3 | `int64` | From its first Speak to at_ms (a duration). |
| `egress_delay_ms` | 4 | optional `int64` | The latency of the mixer the speaker plays to its participant through, when it has one (a duration): about how much after at_ms the audio leaves synauson. |

### AgentWordsPlayed

Words of an utterance that fully played, in order. Joined, an
utterance's AgentWordsPlayed are the words of its text that were heard;
none follows its AgentUtteranceDone, AgentUtteranceInterrupted or
AgentUtteranceFailed.

| Field | Number | Type | Description |
|---|---|---|---|
| `utterance_id` | 1 | `string` | The utterance's id. |
| `words` | 2 | repeated [`PlayedWord`](#playedword) | The words, in order. |

### PlayedWord

One word of an utterance that fully played.

| Field | Number | Type | Description |
|---|---|---|---|
| `text` | 1 | `string` | The word as sent, punctuation attached ("Hello,"); an entity spoken as several words is one ("$42.50"). |
| `text_start` | 2 | `int64` | Its range in the utterance's text (its Speaks' text concatenated), in Unicode code points, not UTF-16 units: in Java or JavaScript, index the text by code point (`String.offsetByCodePoints`) for any text outside the Basic Multilingual Plane, such as emoji. |
| `text_end` | 3 | `int64` | The end of its range (exclusive), in code points. |
| `start_ms` | 4 | `int64` | Where it starts in the utterance's own audio (a duration from its first sample; gaps in playback don't move it). |
| `end_ms` | 5 | `int64` | Where it ends in the utterance's own audio (a duration from its first sample). |

### AgentUtteranceDone

An utterance played to its end.

| Field | Number | Type | Description |
|---|---|---|---|
| `utterance_id` | 1 | `string` | The utterance's id. |
| `audio_ms` | 2 | `int64` | Its audio's length (a duration). |
| `at_ms` | 3 | `int64` | When its last sample played. |
| `underrun_ms` | 4 | `int64` | Silence inside it while synthesis fell behind playback (a duration). |

### AgentUtteranceInterrupted

An utterance stopped before its end; nothing more of it plays.

| Field | Number | Type | Description |
|---|---|---|---|
| `utterance_id` | 1 | `string` | The utterance's id. |
| `reason` | 2 | [`UtteranceInterruptReason`](#utteranceinterruptreason) | Why it stopped. |
| `heard_text` | 3 | `string` | The text up to the end of its last fully played word, as sent. |
| `heard_text_end` | 4 | `int64` | `heard_text`'s length in Unicode code points (not UTF-16 units, see `PlayedWord.text_start`): where the unheard text starts. |
| `heard_ms` | 5 | `int64` | How much of its audio played (a duration), partly heard words included. |

### AgentUtteranceFailed

An utterance failed; nothing more of it plays.

| Field | Number | Type | Description |
|---|---|---|---|
| `utterance_id` | 1 | `string` | The utterance's id. |
| `code` | 2 | [`UtteranceFailure`](#utterancefailure) | Why it failed. |
| `message` | 3 | `string` | What happened, for people. Don't match on it. |

### AgentStreamEndReason

Why an agent stream ended. May gain values: accept ones you don't know.

| Value | Number | Description |
|---|---|---|
| `AGENT_STREAM_END_REASON_UNSPECIFIED` | 0 | Never sent. |
| `AGENT_STREAM_END_REASON_PARTICIPANT_REMOVED` | 1 | The participant was removed. |
| `AGENT_STREAM_END_REASON_CONFERENCE_TERMINATED` | 2 | The conference was terminated, by `TerminateConference` or by a server shutdown. |

### TurnResumeCause

Why an eager end of turn was taken back. May gain values: accept ones you
don't know.

| Value | Number | Description |
|---|---|---|
| `TURN_RESUME_CAUSE_UNSPECIFIED` | 0 | Never sent. |
| `TURN_RESUME_CAUSE_SPEECH` | 1 | The participant spoke again, and turn detection didn't call the pause the turn's end (synauson waits up to 250 ms for a decision in flight). |
| `TURN_RESUME_CAUSE_WORDS` | 2 | Committed words differ from the eager end of turn's. |

### TurnEndReason

Why a turn ended. May gain values: accept ones you don't know.

| Value | Number | Description |
|---|---|---|
| `TURN_END_REASON_UNSPECIFIED` | 0 | Never sent. |
| `TURN_END_REASON_MODEL` | 1 | Turn detection's probability for a pause reached end_of_turn_threshold. |
| `TURN_END_REASON_MANUAL` | 2 | `ForceEndTurn`. |
| `TURN_END_REASON_TIMEOUT` | 3 | Silence for end_of_turn_timeout_ms after a speech end. |
| `TURN_END_REASON_STREAM_ENDED` | 4 | The participant or the conference went with the turn open. |

### SpeakRelease

What a Speak's text ends.

| Value | Number | Description |
|---|---|---|
| `SPEAK_RELEASE_UNSPECIFIED` | 0 | Unset: treated as `SPEAK_RELEASE_NONE`. |
| `SPEAK_RELEASE_NONE` | 1 | Nothing: more text may follow, and the speaker holds back what could still change (a number still being written). |
| `SPEAK_RELEASE_FLUSH` | 2 | Speak everything sent so far now; the utterance stays open. |
| `SPEAK_RELEASE_END` | 3 | The utterance's text is complete; `AgentUtteranceDone` follows its playback. |

### UtteranceInterruptReason

Why an utterance stopped before its end. May gain values: accept ones
you don't know.

| Value | Number | Description |
|---|---|---|
| `UTTERANCE_INTERRUPT_REASON_UNSPECIFIED` | 0 | Never sent. |
| `UTTERANCE_INTERRUPT_REASON_CANCELLED` | 1 | `CancelUtterance`. |
| `UTTERANCE_INTERRUPT_REASON_PREEMPTED` | 2 | A new utterance started while it was preemptible. |
| `UTTERANCE_INTERRUPT_REASON_STREAM_ENDED` | 3 | The participant or the conference went (sent before AgentStreamEnded). |

### UtteranceFailure

Why an utterance failed. May gain values: accept ones you don't know.

| Value | Number | Description |
|---|---|---|
| `UTTERANCE_FAILURE_UNSPECIFIED` | 0 | Never sent. |
| `UTTERANCE_FAILURE_TTS_UNAVAILABLE` | 1 | The speaker's text-to-speech engine is gone. |
| `UTTERANCE_FAILURE_SYNTHESIS_FAILED` | 2 | The model failed on its text. |
| `UTTERANCE_FAILURE_UNSPEAKABLE_TEXT` | 3 | Its text has nothing to say, or a word too long for the model. |
| `UTTERANCE_FAILURE_TTS_CAPACITY` | 4 | The machine's text-to-speech capacity was in use when it was to start. |

## synauson/v1/capabilities.proto

### GetCapabilitiesRequest

Ask what this instance may use.

### GetCapabilitiesResponse

What this synauson instance is and may use right now, and how much is in
use.

Enums and the string fields documented with a list of values may gain
values in later releases: clients must accept values they don't know.

| Field | Number | Type | Description |
|---|---|---|---|
| `server_version` | 14 | `string` | The server's release, as semantic versioning ("1.8.0"). |
| `api_version` | 15 | `string` | The release of this API (the synauson/api tag, as "1.0.0") the server implements. A client built from a newer release may find RPCs that fail with UNIMPLEMENTED and fields the server never sets. |
| `license` | 1 | [`LicenseInfo`](#licenseinfo) | The license in force and its standing. |
| `limits_scope` | 2 | [`LimitsScope`](#limitsscope) | What the license's limits count over. |
| `overdraft` | 3 | `double` | Fraction above the purchased part of each limit (sessions and conferences alike) still admitted as a burst, reported as overage. |
| `capabilities` | 6 | repeated [`CapabilityInfo`](#capabilityinfo) | Each capability a license can grant, and whether new work may use it. |
| `models` | 7 | repeated [`ModelInfo`](#modelinfo) | Each model the license entitles, or could, and its state on this instance. |
| `onnx_runtime` | 8 | [`OnnxRuntimeInfo`](#onnxruntimeinfo) | The ONNX Runtime library every model runs on. |
| `stt` | 9 | [`SttCapacityInfo`](#sttcapacityinfo) | This machine's speech-to-text capacity and its pool. |
| `sessions` | 10 | [`PoolUsage`](#poolusage) | The license's pool of concurrent AI sessions: participants using any AI capability, one session each. |
| `resources` | 11 | [`ResourcesInfo`](#resourcesinfo) | What this instance may use, detected at startup: its CPU budget, cores, CPU features and memory limit, with their sources. |
| `calibration` | 12 | [`CalibrationInfo`](#calibrationinfo) | The calibration cache (model timings kept in the state directory across restarts) and the voice activity and turn detection timings in force. Speech-to-text's are in stt. |
| `tts` | 13 | [`TtsCapacityInfo`](#ttscapacityinfo) | This machine's text-to-speech pool and its cap on speaking utterances. |
| `usage_service` | 16 | [`UsageServiceInfo`](#usageserviceinfo) | This instance's standing with the usage service: its share of each of the license's pools and the time it has left to reconnect. |
| `conferences` | 17 | [`PoolUsage`](#poolusage) | The license's pool of concurrent conferences: every conference, with or without AI, from its start until it ends. Both pools apply: a conference takes one conference, and each participant in it using AI takes one AI session too. |

### UsageServiceInfo

The usage service (usage.synauson.com) as this instance sees it. Every
instance reports its AI session and conference counts there every 30
seconds and is leased a share of each of the license's two pools. While reports can't get
through, the instance keeps admitting against the last share it held,
with its burst, for 7 days after the last report that got through;
calls in progress are never stopped.

| Field | Number | Type | Description |
|---|---|---|---|
| `contact` | 1 | [`UsageContact`](#usagecontact) | Its contact with the service. |
| `last_contact_time` | 2 | `google.protobuf.Timestamp` | The last contact the 7 days count from: the newest report the service accepted, moved forward while Synauson's own outage notice is up. Unset for an air-gapped license. |
| `grace_end_time` | 3 | `google.protobuf.Timestamp` | When new calls stop unless a report gets through first. Unset for an air-gapped license. |
| `share` | 4 | optional `int32` | This instance's share of the license's sessions, while leased; absent when unlimited or not leased. |
| `share_ceiling` | 5 | optional `int32` | The most sessions this instance may hold: its share plus the burst on the purchased part of it (the Free base has none). |
| `pool_in_use` | 6 | optional `int32` | Sessions in use across all the license's instances at the last report. |
| `instances` | 7 | optional `int32` | Instances holding a share at the last report. |
| `pause_time` | 8 | `google.protobuf.Timestamp` | Since when Synauson's signed notice says the usage service itself is down: the 7 days are paused until it is cleared. Unset otherwise. |
| `refuse_time` | 9 | `google.protobuf.Timestamp` | Since when the usage service refuses this license's reports (the licensing server refused it): the 7 days run from no later than this. Unset otherwise. |
| `problem` | 10 | optional `string` | Why the last report failed. |
| `conference_share` | 11 | optional `int32` | This instance's share of the license's conferences, while leased; absent when unlimited or not leased. An instance that holds no share, leased or kept from its last lease, starts no conference, unless the conference pool is unlimited or the license air-gapped. |
| `conference_share_ceiling` | 12 | optional `int32` | The most conferences this instance may hold: its share plus the burst on the purchased part of it (the Free base has none). |
| `conference_pool_in_use` | 13 | optional `int32` | Conferences in use across all the license's instances at the last report. |

### CalibrationInfo

The calibration cache and the detector timings in force.

| Field | Number | Type | Description |
|---|---|---|---|
| `file` | 1 | optional `string` | The cache file in the state directory; absent when the server runs without one. |
| `recalibrate` | 2 | `bool` | Whether this start ignores the cached timings (the operator asked to recalibrate). |
| `vad` | 3 | [`DetectorTiming`](#detectortiming) | One voice activity chunk (32 ms of audio), once timed. |
| `turn_detection` | 4 | [`DetectorTiming`](#detectortiming) | One turn detection decision, once timed. |

### DetectorTiming

How long one detector run takes on this machine.

| Field | Number | Type | Description |
|---|---|---|---|
| `model` | 1 | `string` | The model timed, by its catalog id. |
| `threads` | 2 | `int32` | The inference threads it ran on. |
| `run_ms` | 3 | `double` | How long one run took, in ms (a duration). |
| `source` | 4 | [`ValueSource`](#valuesource) | AUTO (measured on this start) or CACHED (on an earlier one, read from the calibration cache). |

### ResourcesInfo

What this instance may use, detected at startup.

| Field | Number | Type | Description |
|---|---|---|---|
| `cpu_budget` | 1 | `double` | Cores this instance may use, fractional with a CPU quota: the smallest of the control group's CPU quota (its own and its ancestors'), its CPU set, the process's CPU affinity, a Windows job's hard CPU cap and the CPU count, or the operator's override. |
| `cpu_source` | 2 | [`ValueSource`](#valuesource) | AUTO (detected) or OVERRIDE (set by the operator). |
| `limited_by` | 3 | `string` | What set the budget: "cpu_max" (a control group CPU quota), "cpuset", "affinity", "job_cpu_rate" (a Windows job object's CPU cap), "std_parallelism" (the CPU count) or "override". Others may be added. |
| `cores` | 4 | `int32` | Whole cores the model pools size by: the budget rounded down, at least 1. |
| `logical_cpus` | 5 | `int32` | Logical CPUs this instance may run on. |
| `physical_cores` | 6 | optional `int32` | Physical cores among the CPUs this instance may run on, where known. |
| `performance_cpus` | 7 | optional `int32` | Performance CPUs on a hybrid processor; absent with one core type. |
| `cpu_model` | 8 | `string` | The processor's model name. |
| `cpu_flags` | 9 | repeated `string` | The instruction set extensions the inference kernels are picked by: "avx2", "avx512f", "avx512vnni", "avxvnni", "amx_tile", "amx_int8"; on ARM64 "dotprod", "i8mm", "bf16". Others may be added. |
| `memory_limit_bytes` | 10 | optional `int64` | The memory limit (the control group's, a Windows job's, or the operator's override), in bytes; absent with none. |
| `memory_source` | 11 | [`ValueSource`](#valuesource) | AUTO (detected) or OVERRIDE (set by the operator). |

### LicenseInfo

The license in force and its standing.

| Field | Number | Type | Description |
|---|---|---|---|
| `state` | 1 | [`LicenseState`](#licensestate) | The standing. |
| `description` | 2 | `string` | One line describing the license and its state, for people. |
| `license_id` | 3 | optional `string` | The license's id, when there is a license. |
| `display_name` | 4 | optional `string` | The license's name, for people, when it has one. |
| `source` | 5 | optional [`LicenseSource`](#licensesource) | Where the license file came from, when there is one; absent when no license file is in force (rejected). Unlike `plan`, this field has no value in some states, so it keeps presence; LICENSE_SOURCE_UNSPECIFIED is still never sent. |
| `file_expire_time` | 6 | `google.protobuf.Timestamp` | When the license file in use stops being valid offline. |
| `license_expire_time` | 7 | `google.protobuf.Timestamp` | The license's own expiry, if it has one. |
| `days_remaining` | 9 | optional `int32` | Whole days until the license expires, or (while LICENSE_STATE_OFFLINE) until new calls stop without contact. |
| `problem` | 10 | optional `string` | What needs attention: a refused renewal, a failing license check, or why new work is refused. |
| `plan` | 11 | [`LicensePlan`](#licenseplan) | The plan the license is on now; always set. FREE once a Free or paid license expires; still DEVELOPER once a developer license expires; the license's own plan while it is disconnected (`state` says nothing new starts); UNLICENSED when no license is in force (rejected). |

Reserved (removed, never reused): number 8.

### PoolUsage

One of the license's pools (concurrent AI sessions or concurrent
conferences), and this instance's use of it. A participant using any AI
capability takes one session, whatever it uses; a conference takes one
conference, whether or not it uses AI. Running sessions and conferences
are never stopped; a new one past the limit and its burst is refused
(`SESSION_LIMIT_REACHED`, `CONFERENCE_POOL_LIMIT_REACHED`).

| Field | Number | Type | Description |
|---|---|---|---|
| `limit` | 1 | optional `int32` | The Free base plus the purchased units; absent means unlimited. |
| `in_use` | 2 | `int32` | Units in use now on this instance. |
| `ceiling` | 3 | optional `int32` | The most admitted at once: the base plus the purchased units and their overdraft (the burst applies to purchased units only); absent when unlimited. |
| `level` | 4 | [`PoolLevel`](#poollevel) | How close the units in use are to the limit. |
| `peak` | 5 | `int32` | The most units at once since the server started, for true-up. |
| `peak_time` | 6 | `google.protobuf.Timestamp` | When the peak was first reached; unset before the first unit. |
| `base` | 7 | `int32` | The Free base every license has in this pool, with no burst (the Free plan's sessions, with every AI feature, or its conferences); 0 while the license starts nothing new. |
| `purchased` | 8 | optional `int32` | Units bought on top of the base; absent means unlimited. |

### Usage

A capped count and how much of it is in use.

| Field | Number | Type | Description |
|---|---|---|---|
| `limit` | 1 | optional `int32` | The cap; absent means unlimited. |
| `in_use` | 2 | `int32` | How many are in use now. |

### CapabilityInfo

One capability a license can grant.

| Field | Number | Type | Description |
|---|---|---|---|
| `code` | 1 | `string` | Its entitlement code: FEATURE_VAD, FEATURE_TURN_DETECTION, FEATURE_STT or FEATURE_TTS. Others may be added. |
| `entitled` | 2 | `bool` | Whether new work may use it: every license grants every capability, so false only while the license starts nothing new. |
| `included_by` | 4 | optional `string` | The entitlement code that grants it when the license doesn't name it itself. Absent when named directly or not entitled. |

### ModelInfo

One model and its state on this instance. Licensed models download in
the background, so a model can be missing for a while after a start.

| Field | Number | Type | Description |
|---|---|---|---|
| `id` | 1 | `string` | The model's catalog id. |
| `variant` | 2 | `string` | The model's variant: the build or quantization the server picked for this machine ("cpu", "int8", "fp32"), which is also its directory in the model store. A machine of another kind may get another variant of the same model. Others may be added. |
| `release` | 3 | `string` | The model's version: its release, as the catalog numbers it. |
| `state` | 4 | [`ModelState`](#modelstate) | Its state. A failed download stays MISSING or INVALID, with the error and the retry time in `detail`. |
| `detail` | 5 | optional `string` | Why it is in that state, when it isn't ready. |

### OnnxRuntimeInfo

The ONNX Runtime library the server loaded; every model runs on it.

| Field | Number | Type | Description |
|---|---|---|---|
| `state` | 1 | [`OnnxRuntimeState`](#onnxruntimestate) | Whether the library loaded. |
| `version` | 2 | optional `string` | The loaded library's version. |
| `path` | 3 | optional `string` | The file it was loaded from, when the platform reports it. |
| `shipped_version` | 4 | `string` | The release synauson ships and tests. Another version runs, but model speed and outputs can differ. |
| `detail` | 5 | optional `string` | Why it is unavailable, or another ONNX Runtime library loaded in the process. |

### SttCapacityInfo

How many speech-to-text streams this machine transcribes in real time,
and the pool that does it: measured when the pool starts (a timed decode,
and the private memory each worker's model adds), or set by the operator.
Each speech-to-text participant also takes a license session.

| Field | Number | Type | Description |
|---|---|---|---|
| `state` | 1 | [`PoolState`](#poolstate) | The pool's state; participants with `stt` need it READY. |
| `workers` | 2 | optional `int32` | Decoding workers in the pool, once known. |
| `threads_per_worker` | 3 | optional `int32` | Inference threads each worker uses, once known. |
| `real_time_factor` | 4 | optional `double` | One stream's decode time over audio time, when measured. |
| `streams` | 5 | [`Usage`](#usage) | The stream cap (once known) and the streams in use. |
| `detail` | 6 | optional `string` | Why it is idle, or failed. |
| `model_bytes` | 8 | optional `int64` | Private memory each worker's model adds, in bytes, when measured (Linux). Model weights shared through the model store are paid once, not per worker, and are not counted here: they are shared_model_bytes. |
| `limited_by` | 9 | optional `string` | What set the worker count: "cpu", "memory" or "operator". Others may be added. |
| `turn_flush` | 10 | `bool` | Whether turns close early on forecasts of their last words (the turn flush, set by the operator). |
| `forecast_reserve` | 11 | optional `double` | Decoding the stream cap reserves per stream for forecasts (the turn flush's and eager end of turn's, at most one per pause), as a share of the stream's own: 0 when both are off or the model can't forecast; absent when not calibrated. |
| `shared_model_bytes` | 12 | optional `int64` | Memory of the model weights shared through the model store, in bytes, when measured (Linux): paid once by every worker and every instance on the host using the same store, so the pool's model memory is about workers x model_bytes + shared_model_bytes. 0 when the weights load privately into each worker. |
| `source` | 13 | optional [`ValueSource`](#valuesource) | Where the capacity came from: AUTO (timed on this start), CACHED (every timing read from the calibration cache) or OVERRIDE (all set by the operator); absent until the capacity is known. It keeps presence for that state; VALUE_SOURCE_UNSPECIFIED is still never sent. |
| `eager` | 14 | `bool` | Whether participants with stt may turn eager end of turn on: the operator allowed it, and the stream cap reserves decoding for its forecasts. With the turn flush on they may anyway: its reserve covers them. |

### TtsCapacityInfo

The text-to-speech pool and its cap on utterances synthesising at once,
from the cores by a fixed rule or set by the operator. A speaker holds a
place only while it speaks; a participant with tts also takes a license
session.

| Field | Number | Type | Description |
|---|---|---|---|
| `state` | 1 | [`PoolState`](#poolstate) | The pool's state; participants with `tts` need it READY. |
| `workers` | 2 | optional `int32` | Synthesis workers in the pool, once known. |
| `threads_per_worker` | 3 | optional `int32` | Inference threads each worker uses, once known. |
| `streams` | 4 | [`Usage`](#usage) | The cap on utterances synthesising at once, and how many are. |
| `detail` | 5 | optional `string` | Why it is idle, or failed. |

### LimitsScope

What a license's limits count over. May gain values: accept ones
you don't know.

| Value | Number | Description |
|---|---|---|
| `LIMITS_SCOPE_UNSPECIFIED` | 0 | Not set; never sent. |
| `LIMITS_SCOPE_LICENSE` | 1 | All instances of the license, at every site: each reports to the usage service, which leases it a share of each pool (usage_service). |
| `LIMITS_SCOPE_INSTANCE` | 2 | This instance alone: an air-gapped license, which sends no reports. |

### UsageContact

This instance's contact with the usage service. May gain values: accept
ones you don't know.

| Value | Number | Description |
|---|---|---|
| `USAGE_CONTACT_UNSPECIFIED` | 0 | Not set; never sent. |
| `USAGE_CONTACT_LEASED` | 1 | A share leased within the last 10 minutes. |
| `USAGE_CONTACT_UNREPORTED` | 2 | Reports are not getting through: the last share and its burst hold until grace_end_time. |
| `USAGE_CONTACT_LAPSED` | 3 | 7 days without contact: no new conference or participant starts until a report gets through. |
| `USAGE_CONTACT_AIR_GAPPED` | 4 | An air-gapped license, arranged with Synauson, which sends no reports. |

### ValueSource

Where a value came from. May gain values: accept ones you don't know.

| Value | Number | Description |
|---|---|---|
| `VALUE_SOURCE_UNSPECIFIED` | 0 | Not set; never sent. |
| `VALUE_SOURCE_AUTO` | 1 | Detected or measured on this start. |
| `VALUE_SOURCE_CACHED` | 2 | Measured on an earlier start and read from the calibration cache. |
| `VALUE_SOURCE_OVERRIDE` | 3 | Set by the operator. |

### PoolState

The state of a model pool (speech-to-text or text-to-speech). May gain
values: accept ones you don't know.

| Value | Number | Description |
|---|---|---|
| `POOL_STATE_UNSPECIFIED` | 0 | Not set; never sent. |
| `POOL_STATE_IDLE` | 1 | Not started: no license or model yet; `detail` says which. |
| `POOL_STATE_LOADING` | 2 | Calibrating and loading the workers' models. Participants that need the pool are refused with `MODEL_LOADING` until it is ready. |
| `POOL_STATE_READY` | 3 | Running. |
| `POOL_STATE_FAILED` | 4 | Failed to start; the next participant that needs it tries again. |

### LicenseState

A license's standing. May gain values: accept ones you don't know.
Calls in progress continue in every state.

| Value | Number | Description |
|---|---|---|
| `LICENSE_STATE_UNSPECIFIED` | 0 | Not set; never sent. |
| `LICENSE_STATE_VALID` | 1 | In force. |
| `LICENSE_STATE_EXPIRING` | 2 | In force, with full function, and within 14 days of expiry. |
| `LICENSE_STATE_OFFLINE` | 3 | Usage reports have not reached usage.synauson.com for an hour or more. Full function until 7 days after the last one that did, paused while Synauson's own outage notice is up (usage_service says when). |
| `LICENSE_STATE_EXPIRED` | 4 | Expired. A Free or paid license runs on the Free plan: every AI feature in the Free pools (`PoolUsage.base`), with no burst. A developer license starts nothing new until Synauson renews it (`LICENSE_EXPIRED`). |
| `LICENSE_STATE_DISCONNECTED` | 5 | 7 days without a report reaching usage.synauson.com: no new conference or participant starts until one does (`LICENSE_DISCONNECTED`). |
| `LICENSE_STATE_INVALID_KEPT_LAST_VALID` | 6 | A renewal brought a license that is illegal or can't be verified; the last valid one stays in force. |
| `LICENSE_STATE_REJECTED` | 7 | The license was rejected: nothing new starts (`LICENSE_REJECTED`). |

### LicenseSource

Where the license file in use came from. May gain values: accept ones you
don't know.

| Value | Number | Description |
|---|---|---|
| `LICENSE_SOURCE_UNSPECIFIED` | 0 | Not set; never sent. |
| `LICENSE_SOURCE_SERVER` | 1 | Checked out from the licensing service by this process. |
| `LICENSE_SOURCE_CACHE` | 2 | The copy kept from an earlier check-out. |
| `LICENSE_SOURCE_PROVIDED` | 3 | A file the operator provided. |

### LicensePlan

The plan a license is on. May gain values: accept ones you don't know.

| Value | Number | Description |
|---|---|---|
| `LICENSE_PLAN_UNSPECIFIED` | 0 | Not set; never sent. |
| `LICENSE_PLAN_FREE` | 1 | The Free plan: the Free base of concurrent AI sessions and of concurrent conferences (`PoolUsage.base`), with every AI feature and no burst. |
| `LICENSE_PLAN_PAID` | 2 | A paid plan: sessions or conferences bought on top of the Free base, or unlimited. |
| `LICENSE_PLAN_DEVELOPER` | 3 | A developer license, for development and testing only, not for production use: the Free plan's pools for one year. At expiry it starts nothing new until Synauson renews it (`LICENSE_EXPIRED`). |
| `LICENSE_PLAN_UNLICENSED` | 4 | No license in force: the licensing service rejected it, so nothing new starts (`LICENSE_REJECTED`). |

### PoolLevel

How close a license pool's units in use are to its limit. May gain
values: accept ones you don't know.

| Value | Number | Description |
|---|---|---|
| `POOL_LEVEL_UNSPECIFIED` | 0 | Not set; never sent. |
| `POOL_LEVEL_OK` | 1 | Below 80% of the limit, or no limit. |
| `POOL_LEVEL_NEAR_LIMIT` | 2 | From 80% of the limit. |
| `POOL_LEVEL_OVERAGE` | 3 | Above the limit, within the overdraft. |
| `POOL_LEVEL_FULL` | 4 | At the ceiling: new units are refused, sessions with `SESSION_LIMIT_REACHED` and conferences with `CONFERENCE_POOL_LIMIT_REACHED`. |

### ModelState

A model's state on this instance. May gain values: accept ones you don't
know.

| Value | Number | Description |
|---|---|---|
| `MODEL_STATE_UNSPECIFIED` | 0 | Not set; never sent. |
| `MODEL_STATE_READY` | 1 | In the model store, verified and usable. |
| `MODEL_STATE_DOWNLOADING` | 2 | Downloading, by this process or another sharing the model store. |
| `MODEL_STATE_MISSING` | 3 | Not in the model store. |
| `MODEL_STATE_INVALID` | 4 | In the model store but failing verification. |
| `MODEL_STATE_NOT_ENTITLED` | 5 | The license doesn't entitle it. |

### OnnxRuntimeState

Whether the ONNX Runtime library loaded. May gain values: accept ones
you don't know.

| Value | Number | Description |
|---|---|---|
| `ONNX_RUNTIME_STATE_UNSPECIFIED` | 0 | Not set; never sent. |
| `ONNX_RUNTIME_STATE_LOADED` | 1 | Loaded; models can run. |
| `ONNX_RUNTIME_STATE_UNAVAILABLE` | 2 | Not loaded: `detail` says why. Participants that need a model are refused with `ONNX_RUNTIME_UNAVAILABLE`. |

## synauson/v1/conference.proto

### StartConferenceRequest

Start a conference.

Errors: `INVALID_ID`, `CONFERENCE_ALREADY_EXISTS`,
`CONFERENCE_LIMIT_REACHED` (the server's own cap),
`CONFERENCE_POOL_LIMIT_REACHED` (the license's conferences),
`LICENSE_REJECTED`, `LICENSE_DISCONNECTED`, `LICENSE_EXPIRED` (the
license starts nothing new), `SERVER_SHUTTING_DOWN`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The new conference's id, chosen by the caller. |

### StartConferenceResponse

The conference started.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | The conference's id, as requested. |

### TerminateConferenceRequest

End a conference.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The conference to end. |

### TerminateConferenceResponse

The conference ended: its participants are gone and its streams closed.

### GetConferenceRequest

Ask for a conference.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The conference to describe. |

### GetConferenceResponse

A conference. Mutes, routes and SIP reservations are write-only: this
response doesn't report them.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | The conference's id. |
| `participants` | 2 | repeated [`ParticipantInfo`](#participantinfo) | Its participants, in no particular order; at most the operator's participant cap, when one is set. A SIP reservation not yet connected is not a participant and is left out. |
| `create_time` | 3 | `google.protobuf.Timestamp` | When the conference started. |

### ParticipantInfo

One participant of a conference.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The participant's id. |
| `kind` | 2 | [`ParticipantKind`](#participantkind) | What kind of participant it is. |

### ParticipantKind

What kind of participant it is. May gain values: accept ones you don't
know.

| Value | Number | Description |
|---|---|---|
| `PARTICIPANT_KIND_UNSPECIFIED` | 0 | Not set; never sent. |
| `PARTICIPANT_KIND_FILE` | 1 | Plays an audio file (`AddFileParticipant`). |
| `PARTICIPANT_KIND_RECORDING` | 2 | Records to a WAV file (`AddRecordingParticipant`). |
| `PARTICIPANT_KIND_SIP` | 3 | A SIP call's media (`AddSipParticipant`, `ConnectSipParticipant`). |
| `PARTICIPANT_KIND_WEBRTC` | 4 | A WebRTC peer (`AddWebRtcParticipant`). |

## synauson/v1/detector.proto

### DetectorConfig

The voice-agent features to run on a participant's incoming audio, set
when it is added. Each may be omitted. They form a chain, `vad` <-
`turn_detection` <- `stt` (and `turn_detection` <- `tts`), and each needs
the one below it on the same participant; a participant missing one
fails with `INVALID_ARGUMENT` naming both fields. Synauson never adds one
for you.

Licensing follows the same chain: an entitlement includes everything
below it. A participant with any of them takes one concurrent AI session
from the license's pool, whatever it runs.

Adding a participant with detectors can fail with these reasons, beyond
the add's own:

`INVALID_ARGUMENT`: a detector without the one it needs, an unknown
`tts.voice`, a value out of range; `INVALID_TURN_CONFIG` for `turns`.

`FEATURE_NOT_LICENSED`: the license doesn't grant one of them.

`MODEL_LOADING`: a model, or the speech-to-text or text-to-speech pool,
is still downloading or loading (licensed models download in the
background after a start); retry shortly. Adds never wait.

`MODEL_UNAVAILABLE`, `ONNX_RUNTIME_UNAVAILABLE`: a model or the runtime
can't run until the operator fixes it.

`SESSION_LIMIT_REACHED`, `STT_CAPACITY_REACHED`: the license's concurrent
AI sessions (beyond its burst), or this machine's speech-to-text streams,
are in use.

| Field | Number | Type | Description |
|---|---|---|---|
| `vad` | 1 | [`VadConfig`](#vadconfig) | Voice activity detection: when the participant speaks. |
| `turn_detection` | 2 | [`TurnDetectionConfig`](#turndetectionconfig) | Turn detection: at each speech end, whether the participant finished their turn. Needs `vad` on the same participant, whose speech ends it decides on. Gives the participant an agent stream (`StreamAgentEvents`). |
| `stt` | 3 | [`SttConfig`](#sttconfig) | Streaming speech-to-text (`StreamTranscriptEvents`, and words on the agent stream). Needs `turn_detection` on the same participant, whose turn ends close each `TurnTranscript`. Counts against this machine's speech-to-text capacity. |
| `turns` | 4 | [`TurnConfigUpdate`](#turnconfigupdate) | The agent stream's turn config at the start, over its defaults (`end_of_turn_threshold` from `turn_detection.confidence_threshold`, timeout 5000 ms, eager off with `eager_threshold` 0); the same fields and ranges as `UpdateTurnConfig`. Needs `turn_detection`. Its `end_of_turn_threshold` replaces `turn_detection.confidence_threshold`. |
| `tts` | 5 | [`TtsConfig`](#ttsconfig) | A speaker: text-to-speech into the call (`Speak`, `CancelUtterance`). Needs `turn_detection` on the same participant: its events go on the agent stream. Licensed by FEATURE_TTS. |

### TtsConfig

A participant's speaker.

| Field | Number | Type | Description |
|---|---|---|---|
| `voice` | 1 | optional `string` | The default voice: "en-us-f1" to "en-us-f11" or "en-us-m1" to "en-us-m9" ("en-us-f1" when unset). An unknown one fails the add with `INVALID_ARGUMENT`. |
| `speed` | 2 | optional `float` | The default speaking rate, 0.25 to 4 (1 when unset). |
| `speaker_id` | 3 | optional `string` | The speaker's id as a routing source, for `SetAudioRoutes` (to a recording, say); `participant_id` + ".speaker" when unset, so a participant id over 120 characters needs one (the add fails with `INVALID_ID` otherwise). An id (see `Syn`) that must not be another participant's. The speaker plays to its own participant without a route (a file participant has no output, so its speaker plays only where it is routed); a route from it to its own participant is refused. |

### VadConfig

Voice activity detection settings.

| Field | Number | Type | Description |
|---|---|---|---|
| `threshold` | 1 | optional `float` | Speech probability, in (0, 1), at or above which audio counts as speech; 0.5 when unset. Speech ends when the probability stays below `threshold` - 0.15 for `min_silence_ms`. |
| `min_silence_ms` | 2 | optional `int32` | Silence, in ms (a duration, 0 to 10000), before the speech counts as ended; 300 when unset. Turn detection decides at each speech end, so this sets how soon it can. |
| `min_speech_ms` | 3 | optional `int32` | Speech, in ms (a duration, 0 to 10000), before it counts as started; 100 when unset. |

### TurnDetectionConfig

Turn detection settings.

| Field | Number | Type | Description |
|---|---|---|---|
| `buffered_samples` | 1 | `int32` | Audio (16 kHz samples) the participant must have sent before turn detection decides: 0 means the model's minimum (4000, 250 ms), smaller values are raised to it, and more than 128000 (the model's 8 s window) or below 0 is `INVALID_ARGUMENT`. |
| `confidence_threshold` | 2 | optional `float` | The probability, in [0, 1], at or above which a pause ends the turn; 0.5 when unset, and 0 ends the turn at every pause. `DetectorConfig.turns.end_of_turn_threshold` replaces it when set. |

### SttConfig

Speech-to-text settings.

| Field | Number | Type | Description |
|---|---|---|---|
| `turn_drain_ms` | 1 | optional `int32` | How long a turn's transcript waits, after the turn ends, for the transcription to settle the turn's text: 0 to 10000 ms of wall time, 1000 when unset. A turn that runs out closes with `complete` false. |

## synauson/v1/errors.proto

### ErrorReason

Every error reason synauson sends, for reference: no message carries this
enum. A reason travels as a string, the value's name: in the
`google.rpc.ErrorInfo` every failed call's status carries (domain
"synauson.com"), or in `AgentError.reason` on the agent stream. Each
value's comment gives the status code, the metadata keys (lowerCamelCase,
string values) and an example.

For example, `GetConference` with an unknown id fails with NOT_FOUND and
the details hold:

    {"@type": "type.googleapis.com/google.rpc.ErrorInfo",
     "reason": "CONFERENCE_NOT_FOUND", "domain": "synauson.com",
     "metadata": {"conferenceId": "call-42"}}

Match on the reason, never on the status code or the message. A reason
keeps its status code and its metadata keys. Later releases may add
reasons and metadata keys: handle a reason you don't know by its status
code.

| Value | Number | Description |
|---|---|---|
| `ERROR_REASON_UNSPECIFIED` | 0 | Not a reason; never sent. |
| `INVALID_ARGUMENT` | 1 | A field of the request is invalid: empty when it is required, out of range, malformed or unsupported. Status INVALID_ARGUMENT; when synauson can name the one field at fault, metadata `field` holds its path (`options.ice_port_min`, say) and a `google.rpc.BadRequest` field violation names it too. |
| `INVALID_ID` | 2 | An id is empty, longer than 128 characters or has a character outside `A-Z`, `a-z`, `0-9`, `.`, `_` and `-`. Status INVALID_ARGUMENT; metadata `field` (`participant_id`, say), with a BadRequest field violation. |
| `INVALID_TURN_CONFIG` | 3 | `UpdateTurnConfig` or `DetectorConfig.turns`: a value is out of range, or eager end of turn isn't allowed; the config is unchanged. Status INVALID_ARGUMENT. |
| `INVALID_SPEAK` | 4 | `Speak`: a request the speaker can't take (text over its cap, voice or speed after the first Speak, an unknown voice, a speed out of range, more than 64 utterances held, playing or queued). Status INVALID_ARGUMENT; metadata `utteranceId`. |
| `CONFERENCE_NOT_FOUND` | 20 | No conference has the id. Status NOT_FOUND; metadata `conferenceId` ("call-42"). |
| `PARTICIPANT_NOT_FOUND` | 21 | The conference has no participant with the id, or none of the kind the call needs (a SIP call for `GetSipStats`, say). Status NOT_FOUND; metadata `conferenceId`, `participantId`. |
| `SIP_RESERVATION_NOT_FOUND` | 22 | `ConnectSipParticipant`: the id has no reservation. Status NOT_FOUND; metadata `conferenceId`, `participantId`. |
| `FILE_NOT_FOUND` | 23 | A `file:` URI names a file that doesn't exist. Status NOT_FOUND; metadata `uri` (its first 512 characters). |
| `UNKNOWN_UTTERANCE` | 24 | `CancelUtterance`: an id the speaker never had. Status NOT_FOUND; metadata `utteranceId`. |
| `CONFERENCE_ALREADY_EXISTS` | 30 | `StartConference`: the id is in use. Status ALREADY_EXISTS; metadata `conferenceId`. |
| `PARTICIPANT_ALREADY_EXISTS` | 31 | The id is a participant, a SIP reservation or a speaker id in the conference already. Status ALREADY_EXISTS; metadata `conferenceId`, `participantId`. |
| `CONFERENCE_LIMIT_REACHED` | 40 | `StartConference`: the server runs as many conferences as its operator allows; end one or use another instance. The operator's own cap on this server, not the license's (that is `CONFERENCE_POOL_LIMIT_REACHED`). Status RESOURCE_EXHAUSTED; metadata `limit` ("100"). |
| `PARTICIPANT_LIMIT_REACHED` | 41 | The conference has as many participants and SIP reservations as the operator allows. Status RESOURCE_EXHAUSTED; metadata `conferenceId`, `limit`. |
| `RTP_PORTS_EXHAUSTED` | 42 | No local RTP port pair is free for a SIP participant. Status RESOURCE_EXHAUSTED; metadata `portMin`, `portMax` (the operator's RTP port range). |
| `SESSION_LIMIT_REACHED` | 43 | The license's concurrent AI sessions, with its burst, are in use; end a session or raise the license. (No share of the pool leased yet is `LICENSE_SHARE_PENDING`.) Status RESOURCE_EXHAUSTED; metadata `inUse`, `limit`, `ceiling` (the most with the burst), `scope` (what the limit counts over: "all instances of this license", or "this instance" for an air-gapped license) and `license` (one line describing the license). |
| `STT_CAPACITY_REACHED` | 44 | This machine's speech-to-text streams are all in use. Status RESOURCE_EXHAUSTED; metadata `inUse`, `limit`. |
| `SUBSCRIBER_LAGGED` | 45 | A file, voice activity, turn detection, transcript, DTMF or ICE candidate stream's subscriber fell behind and was dropped; the events it missed are gone, so subscribe again. Status RESOURCE_EXHAUSTED; metadata `skippedEvents`. |
| `AGENT_SUBSCRIBER_LAGGED` | 46 | `StreamAgentEvents`: the subscriber fell behind and was dropped. Status RESOURCE_EXHAUSTED; metadata `lastSeq`, the last event it got: resume from it. |
| `CONFERENCE_POOL_LIMIT_REACHED` | 47 | `StartConference`: the license's concurrent conferences, with its burst, are in use; end a conference or raise the license. Every live conference counts, with AI or without. (No share of the pool leased yet is `LICENSE_SHARE_PENDING`.) Status RESOURCE_EXHAUSTED; metadata `inUse`, `limit`, `ceiling` (the most with the burst), `scope` (what the limit counts over: "all instances of this license", or "this instance" for an air-gapped license) and `license` (one line describing the license). |
| `LICENSE_REJECTED` | 60 | The license was rejected: nothing new starts until the operator fixes it. Status FAILED_PRECONDITION; metadata `license` (one line describing the license and its problem). |
| `MODEL_UNAVAILABLE` | 61 | A model the participant needs is missing, fails verification, failed to download or failed to load, or the operator turned its pool off; the operator must fix it. Status FAILED_PRECONDITION; metadata `model` (its catalog id, or `stt` or `tts` for a pool). |
| `ONNX_RUNTIME_UNAVAILABLE` | 62 | The ONNX Runtime library isn't loaded, so no model can run. Status FAILED_PRECONDITION. |
| `VAD_REQUIRED` | 63 | `StreamVadEvents`: the participant has no `DetectorConfig.vad`. Status FAILED_PRECONDITION; metadata `conferenceId`, `participantId`. |
| `TURN_DETECTION_REQUIRED` | 64 | The participant has no `DetectorConfig.turn_detection`, so no turn detection events and no agent stream. Status FAILED_PRECONDITION; metadata `conferenceId`, `participantId`. |
| `STT_REQUIRED` | 65 | `StreamTranscriptEvents`: the participant has no `DetectorConfig.stt`. Status FAILED_PRECONDITION; metadata `conferenceId`, `participantId`. |
| `TTS_REQUIRED` | 66 | `Speak`, `CancelUtterance`: the participant has no speaker (no `DetectorConfig.tts`). Status FAILED_PRECONDITION; metadata `conferenceId`, `participantId`. |
| `FILE_PARTICIPANT_REQUIRED` | 67 | `AddPriorityAudioFiles`: the participant isn't a file participant. Status FAILED_PRECONDITION; metadata `conferenceId`, `participantId`. |
| `SIP_RESERVATION_NOT_CONNECTED` | 68 | A route or a recording names a SIP reservation that isn't connected yet. Status FAILED_PRECONDITION; metadata `conferenceId`, `participantId`. |
| `PARTICIPANT_START_FAILED` | 69 | A new participant's media didn't start in time (no audio decoded from a file, SIP media that didn't start, a WebRTC peer that didn't connect); it was not added. Status FAILED_PRECONDITION; metadata `participantId`. |
| `AGENT_STREAM_MISMATCH` | 70 | `StreamAgentEvents`: the cursor's `stream_id` is not the participant's current stream (it was added again). Status FAILED_PRECONDITION; metadata `streamId`, the current one. |
| `UTTERANCE_ENDED` | 71 | `Speak`: the utterance was ended, or has finished, been interrupted or failed; utterance ids are not reused. Status FAILED_PRECONDITION; metadata `utteranceId`. |
| `UTTERANCE_NOT_INTERRUPTIBLE` | 72 | `CancelUtterance`: the utterance was spoken with `interruptible` false. Status FAILED_PRECONDITION; metadata `utteranceId`. |
| `LICENSE_DISCONNECTED` | 73 | No usage report has reached usage.synauson.com for 7 days, so nothing new starts until one does; calls in progress continue. Status FAILED_PRECONDITION; metadata `license` (one line describing the license and its standing). |
| `LICENSE_EXPIRED` | 74 | The license expired and starts nothing new until Synauson renews it; calls in progress continue. Today only a developer license does this: an expired Free or paid license runs on the Free plan instead. Status FAILED_PRECONDITION; metadata `license` (one line describing the license and its standing). |
| `AGENT_REPLAY_EXPIRED` | 80 | `StreamAgentEvents`: the `after_seq` cursor is older than the oldest event the stream keeps; subscribe again without a cursor. Status OUT_OF_RANGE; metadata `oldestSeq`, `lastSeq`, `streamId`. |
| `FEATURE_NOT_LICENSED` | 90 | The license doesn't entitle a model the participant's features need. Every license grants every feature, so this is `LICENSE_REJECTED`, `LICENSE_DISCONNECTED` or `LICENSE_EXPIRED` caught later, when the license changed while the participant was being added. Status PERMISSION_DENIED; metadata `model`, the model's catalog id. |
| `MODEL_LOADING` | 100 | A model the participant needs, or the speech-to-text or text-to-speech pool, is still downloading or loading; retry in a few seconds (`GetCapabilities` shows the state). Status UNAVAILABLE; metadata `model` (its catalog id, or `stt` or `tts` for a pool). |
| `SERVER_SHUTTING_DOWN` | 101 | The server is shutting down and starts nothing new; use another instance. Status UNAVAILABLE. |
| `LICENSE_SHARE_PENDING` | 102 | This instance holds no usable share of one of the license's pools yet (none leased since it started, or the only share it holds was leased under the license's earlier terms), so it starts nothing from that pool until usage.synauson.com leases it one: retry later, or use another instance. Not a full pool (`SESSION_LIMIT_REACHED`, `CONFERENCE_POOL_LIMIT_REACHED`). Status UNAVAILABLE; metadata `pool` ("sessions" or "conferences"), `scope` (what the pool counts over) and `license` (one line describing the license and why it has no share). |
| `INVALID_TOKEN` | 110 | The call has no `authorization: Bearer <token>` metadata, or the token is wrong. Status UNAUTHENTICATED. |
| `INTERNAL` | 120 | A failure inside synauson, not caused by the request. Status INTERNAL. |
| `TURN_DETECTION_FAILED` | 200 | `AgentError`: turn detection stopped on the participant; turns end only by timeout or `ForceEndTurn` from then on. |
| `TURN_DECISION_MISSING` | 201 | `AgentError`: a speech end got no turn detection decision within 2 s; the timeout still ends the turn. |
| `STT_STOPPED` | 202 | `AgentError`: speech-to-text failed on the participant; turns end with the words they had, and later ones without words. |
| `STT_LAGGING` | 203 | `AgentError`: the transcription's backlog passed the participant's `SttConfig.turn_drain_ms` (at least 500 ms); metadata `backlogMs`, `thresholdMs`. Sent again only after the backlog falls to half the threshold. |

## synauson/v1/events.proto

### StreamFileEventsRequest

Subscribe to file playback events. Every event goes to every subscriber;
a subscriber that doesn't take an event within 100 ms is dropped without
affecting the others: its stream ends with `SUBSCRIBER_LAGGED`, so
subscribe again. The stream ends when the conference is terminated, and
sends nothing between events (no heartbeat).

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The conference. |
| `participant_id` | 2 | `string` | The file participant whose events to stream; empty for every file participant of the conference. |

### StreamVadEventsRequest

Subscribe to a participant's voice activity events. Events sent before
the subscription are not replayed, so subscribe before the audio you need
starts. The stream sends nothing between events (no heartbeat), and ends
when the participant or its conference goes. A subscriber that falls
behind gets `SUBSCRIBER_LAGGED` and the stream ends: subscribe again.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND`,
`VAD_REQUIRED`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant whose events to stream. |

### StreamTurnDetectionEventsRequest

Subscribe to a participant's turn detection decisions, delivered as
`StreamVadEventsRequest` describes.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND`,
`TURN_DETECTION_REQUIRED`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant whose decisions to stream. |

### StreamTranscriptEventsRequest

Subscribe to a participant's transcript, delivered as
`StreamVadEventsRequest` describes.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND`,
`STT_REQUIRED`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant whose transcript to stream. |

### FileEvent

One file playback event. Fields 1 to 9 are the envelope; the oneof's
cases take 10 and up.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | The participant's conference. |
| `participant_id` | 2 | `string` | The file participant the event is about. |
| `event_time` | 3 | `google.protobuf.Timestamp` | Wall-clock time the event was made. |
| `playback_started` | 10 | oneof event: [`FilePlaybackStarted`](#fileplaybackstarted) | A file started playing: the participant's own file when it was added, or a priority file (`AddPriorityAudioFiles`). |
| `playback_ended` | 11 | oneof event: [`FilePlaybackEnded`](#fileplaybackended) | A priority file finished playing. |
| `eos` | 12 | oneof event: [`FileEos`](#fileeos) | The participant's own file reached its end (never with `loop_playback`). |
| `error` | 13 | oneof event: [`FileError`](#fileerror) | A file can't be played. |

`oneof event`: What happened. Clients must ignore cases they don't know.

### FilePlaybackStarted

A file started playing.

| Field | Number | Type | Description |
|---|---|---|---|
| `uri` | 1 | `string` | The file's URI. |

### FilePlaybackEnded

A priority file finished playing.

| Field | Number | Type | Description |
|---|---|---|---|
| `uri` | 1 | `string` | The file's URI. |

### FileEos

The participant's own file reached its end.

### FileError

A file can't be played: no audio could be decoded from it when it was
added (the add fails too), its decoder failed while it played, or a
priority file can't be opened or decoded (it is skipped).

| Field | Number | Type | Description |
|---|---|---|---|
| `message` | 1 | `string` | What went wrong, for people. |

### VadEvent

One voice activity event. Fields 1 to 9 are the envelope; the oneof's
cases take 10 and up.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | The participant's conference. |
| `participant_id` | 2 | `string` | The participant the event is about. |
| `event_time` | 3 | `google.protobuf.Timestamp` | Wall-clock time the event was made. |
| `speech_start` | 10 | oneof event: [`VadSpeechStart`](#vadspeechstart) | Speech started. |
| `speech_end` | 11 | oneof event: [`VadSpeechEnd`](#vadspeechend) | Speech ended. |

`oneof event`: What happened. Clients must ignore cases they don't know.

### VadSpeechStart

Speech started: the speech probability stayed at or above
`VadConfig.threshold` for `VadConfig.min_speech_ms`.

| Field | Number | Type | Description |
|---|---|---|---|
| `confidence` | 1 | `float` | The detector's probability for the window that confirmed it. |

### VadSpeechEnd

Speech ended: the probability stayed below the threshold for
`VadConfig.min_silence_ms`.

| Field | Number | Type | Description |
|---|---|---|---|
| `duration_ms` | 1 | `int64` | The length of the speech that ended, from its onset to where the silence began, in ms (a duration). |

### TurnDetectionEvent

One turn detection decision, made at a speech end: whether the
participant finished their turn there. Fields 1 to 9 are the envelope;
the decision takes 10 and up.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | The participant's conference. |
| `participant_id` | 2 | `string` | The participant the decision is about. |
| `event_time` | 3 | `google.protobuf.Timestamp` | Wall-clock time the decision was made. |
| `probability` | 10 | `float` | The model's probability that the turn is complete, in [0, 1]. |
| `turn_complete` | 11 | `bool` | Whether `probability` reached the participant's end of turn threshold (`TurnConfig.end_of_turn_threshold`, so `UpdateTurnConfig` changes it too). |

### TranscriptEvent

A participant's transcript: committed text as it is decoded, and each
turn's text once its turn ends. Its times are transcription audio time:
ms of the participant's audio since transcription started on it, silence
included. That is not the agent stream's conference time; the agent
stream's words carry conference time. Fields 1 to 9 are the envelope;
the oneof's cases take 10 and up.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | The participant's conference. |
| `participant_id` | 2 | `string` | The participant the transcript is of. |
| `event_time` | 3 | `google.protobuf.Timestamp` | Wall-clock time the event was made. |
| `delta` | 10 | oneof event: [`TranscriptDelta`](#transcriptdelta) | Newly committed text. |
| `turn` | 11 | oneof event: [`TurnTranscript`](#turntranscript) | A turn's text. |

`oneof event`: What happened. Clients must ignore cases they don't know.

### TranscriptDelta

Newly committed text, never revised: a participant's deltas concatenate
to its transcript. A growing backlog means the machine can't keep up.

| Field | Number | Type | Description |
|---|---|---|---|
| `text` | 1 | `string` | Word-initial pieces start with a space. Empty when only tentative changed. |
| `tentative` | 2 | `string` | The model's current guess at what follows, replacing any earlier one. Always empty from models that don't revise. |
| `start_ms` | 3 | `int64` | Where the first piece of `text` starts, in transcription audio time. |
| `last_start_ms` | 4 | `int64` | Where the last piece of `text` starts, in transcription audio time. |
| `decoded_ms` | 5 | `int64` | Audio transcribed so far, in transcription audio time. |
| `backlog_ms` | 6 | `int64` | Audio waiting to be transcribed (a duration): how far the transcript runs behind. |

### TurnTranscript

One turn's text: one per turn the participant's agent stream ends (a
complete turn detection decision, the end-of-turn timeout or
ForceEndTurn), sent after the deltas it covers. Each piece of committed
text is in at most one turn, in order, and every committed word reaches
one.

The model commits a word some time after it is spoken, so a turn is cut
where the speech is: its text is the committed text up to where the next
speech started, never splitting a word. Synauson waits up to
`SttConfig.turn_drain_ms` after the turn's end for that text to settle. A
turn's text never starts with punctuation (the end of the sentence
before, which the model commits with the turn's first word), so turns
may end without a period.

A turn closed early (the turn flush) may end with forecast words, sent
before their deltas; if the transcription then commits other words in
their place, those open the next turn. Words no turn end took (a lagging
turn's late words with no speech after them, or what is left at the
audio's end or the participant's removal) get a turn of their own.

| Field | Number | Type | Description |
|---|---|---|---|
| `text` | 1 | `string` | The turn's text, with a leading space. |
| `start_ms` | 2 | `int64` | Where the turn's first piece starts, in transcription audio time; 0 when `text` is empty. |
| `last_start_ms` | 3 | `int64` | Where the turn's last piece starts, in transcription audio time; 0 when `text` is empty. |
| `turn_end_ms` | 4 | `int64` | Where turn detection said the turn ended, in transcription audio time; for a turn of late words, where the turn before it ended. |
| `probability` | 5 | optional `float` | Turn detection's probability for the decision, when the turn ended on one (unset for a timeout, `ForceEndTurn`, or a turn of late words with no turn before it). |
| `complete` | 6 | `bool` | False when the transcription hadn't reached the turn's end within `SttConfig.turn_drain_ms` (or the participant left): its last words open the next turn instead, or a turn of their own if no speech comes before they are transcribed. |

## synauson/v1/participant.proto

### AddFileParticipantRequest

Add a participant that plays an audio file into the conference. Nobody
hears it until a route says so (`SetAudioRoutes`).

Errors: `INVALID_ID`; `INVALID_ARGUMENT` (a URI without a scheme, a
`file:` URI naming a directory, a file that can't be opened or isn't in
an accepted format); `CONFERENCE_NOT_FOUND`; `FILE_NOT_FOUND`;
`PARTICIPANT_ALREADY_EXISTS`; `PARTICIPANT_LIMIT_REACHED`;
`PARTICIPANT_START_FAILED` (no audio could be decoded from the file);
`LICENSE_REJECTED`, `LICENSE_DISCONNECTED`, `LICENSE_EXPIRED` (the
license starts nothing new); `INTERNAL`; and the detector errors
(`DetectorConfig`).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The conference to join. |
| `participant_id` | 2 | `string` | Required. The new participant's id, chosen by the caller. |
| `uri` | 3 | `string` | Required. The file to play, as a URI with a scheme (file:///path/to/audio.wav). Accepted formats: WAV (PCM, A-law or mu-law), Ogg Opus, Ogg Vorbis, FLAC and MP3. A file in any other format fails the add with `INVALID_ARGUMENT`. |
| `loop_playback` | 4 | `bool` | Play the file again from the start each time it ends. |
| `detectors` | 5 | [`DetectorConfig`](#detectorconfig) | Detectors to run on the file's audio. |

### AddFileParticipantResponse

The file participant was added and is playing.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The participant's id, as requested. |

### AddRecordingParticipantRequest

Add a participant that records to a WAV file (16 kHz, 16-bit mono): the
source participant's audio, plus whatever `SetAudioRoutes` routes to it.

Errors: `INVALID_ID`; `INVALID_ARGUMENT` (an empty `output_path`, one
whose directory doesn't exist, a source with no audio of its own such as
another recording); `CONFERENCE_NOT_FOUND`; `PARTICIPANT_NOT_FOUND` (the
source); `PARTICIPANT_ALREADY_EXISTS`; `SIP_RESERVATION_NOT_CONNECTED`
(the source); `PARTICIPANT_LIMIT_REACHED`; `LICENSE_REJECTED`,
`LICENSE_DISCONNECTED`, `LICENSE_EXPIRED` (the license starts nothing
new); `INTERNAL`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The conference to join. |
| `participant_id` | 2 | `string` | Required. The new participant's id, chosen by the caller. |
| `source_participant_id` | 3 | `string` | Required. The participant to record. |
| `output_path` | 4 | `string` | Required. Where to write the WAV file, on the server's file system. An existing file is replaced. |

### AddRecordingParticipantResponse

The recording participant was added and is recording.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The participant's id, as requested. |

### RemoveParticipantRequest

Remove a participant, or release a SIP reservation. Its routes and event
streams end with it.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant to remove. |

### RemoveParticipantResponse

The participant was removed.

### MuteParticipantRequest

Mute or unmute a participant: outgoing only, so listeners stop hearing
it, while its own detectors and speech-to-text still hear it. The mute
belongs to the participant, not to its routes: it holds on every route
from it, including routes added later, until it is unmuted. Unmuting
gives each route back its own `muted` from the routing matrix. A SIP
reservation can be muted too and stays muted once it connects. The mute
is forgotten when the participant is removed, so an id used again starts
unmuted. A speaker id (`TtsConfig.speaker_id`) isn't a participant: mute
its routes in the matrix. Write-only: `GetConference` doesn't report it.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND` (an
id that isn't a participant or reservation in the conference).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The participant to mute or unmute. |
| `muted` | 3 | `bool` | True to mute, false to unmute. |

### MuteParticipantResponse

The mute changed.

### AudioRoute

One route: the source's audio goes to the destination.

| Field | Number | Type | Description |
|---|---|---|---|
| `source_participant_id` | 1 | `string` | The participant (or speaker id) whose audio is sent. |
| `destination_participant_id` | 2 | `string` | The participant that hears it. |
| `muted` | 3 | `bool` | Keep the route but send silence. A route carries audio only when neither this nor the source's `MuteParticipant` mute is set. |

### SetAudioRoutesRequest

Set the conference's whole routing matrix: who hears whom. Synauson
compares it with the current routes: routes not in it are removed, new
ones added, and the others take its `muted`. An empty `routes` removes
every route, and a route left out is removed: always send the whole
matrix. Every route is checked before anything changes, so a refused
matrix leaves the routing as it was. A recording's source and a
speaker's own participant are routed without an entry. Write-only:
`GetConference` doesn't report the routes.

Errors: `INVALID_ID`; `INVALID_ARGUMENT` (more than 4096 routes, a
source with no audio of its own such as a recording, a destination that
can't receive audio such as a file participant, a route from a speaker
to its own participant); `CONFERENCE_NOT_FOUND`; `PARTICIPANT_NOT_FOUND`
(an id the matrix names); `SIP_RESERVATION_NOT_CONNECTED`; `INTERNAL`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The conference. |
| `routes` | 2 | repeated [`AudioRoute`](#audioroute) | Every route the conference should have, at most 4096. |

### SetAudioRoutesResponse

The routes changed.

### AddPriorityAudioFilesRequest

Queue audio files to play on a file participant ahead of its own file.
Its own file pauses while the queue plays, in order, and resumes when the
queue drains; more files sent meanwhile join the queue. Each priority
file gets a `FilePlaybackStarted` and a `FilePlaybackEnded`. One that
can't be opened or decoded, or isn't in a format `AddFileParticipant`
accepts, gets a `FileError` and is skipped: the next one plays, or the
participant's own file resumes.

Errors: `INVALID_ID`; `INVALID_ARGUMENT` (no URIs, more than 64, a URI
as for `AddFileParticipant`); `CONFERENCE_NOT_FOUND`;
`PARTICIPANT_NOT_FOUND`; `FILE_NOT_FOUND` (every URI is checked before
any plays); `FILE_PARTICIPANT_REQUIRED`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The file participant to play them on. |
| `uris` | 3 | repeated `string` | Required. The files to queue, in order, as URIs (see `AddFileParticipantRequest`); 1 to 64. |

### AddPriorityAudioFilesResponse

The files were queued.

## synauson/v1/sip.proto

### AddSipParticipantRequest

Add a SIP call's media as a participant: bidirectional RTP with
parameters the caller already negotiated. The caller does all the SIP
signalling (INVITE, BYE and so on). Codecs: PCMU (payload type 0, 8 kHz),
PCMA (8, 8 kHz) and Opus (96, 48 kHz).

Errors: `INVALID_ID`; `INVALID_ARGUMENT` (an empty or malformed field, an
unsupported codec, a port or DTMF payload type out of range);
`CONFERENCE_NOT_FOUND`; `PARTICIPANT_ALREADY_EXISTS`;
`RTP_PORTS_EXHAUSTED`; `PARTICIPANT_LIMIT_REACHED`;
`PARTICIPANT_START_FAILED`; `LICENSE_REJECTED`, `LICENSE_DISCONNECTED`,
`LICENSE_EXPIRED` (the license starts nothing new); `INTERNAL`; and the
detector errors (`DetectorConfig`).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The conference to join. |
| `participant_id` | 2 | `string` | Required. The new participant's id, chosen by the caller. |
| `remote_ip` | 3 | `string` | Required. The address the peer receives RTP on (its SDP c= line): an IPv4 or IPv6 address, or a host name the server resolves. |
| `remote_rtp_port` | 4 | `int32` | Required. Port the peer receives RTP on (its SDP m= line), 1 to 65535. RTCP goes to the next port. |
| `codec` | 5 | `string` | Required. The codec's RTP payload format name (RFC 3551 and the IANA registry, as in the SDP a=rtpmap line): "PCMU", "PCMA" or "OPUS", in any case. |
| `dtmf_payload_type` | 6 | `int32` | RFC 4733 telephone-event payload type, usually 101; 0 turns RFC 4733 DTMF off. Otherwise it must be in RFC 3551's dynamic range, 96 to 127. |
| `srtp` | 7 | [`SrtpConfig`](#srtpconfig) | SRTP keys, for an encrypted call; unset for plain RTP. |
| `detectors` | 8 | [`DetectorConfig`](#detectorconfig) | Detectors to run on the call's incoming audio. |

### AddSipParticipantResponse

The SIP participant was added and its media is running.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The participant's id, as requested. |
| `local_rtp_port` | 2 | `int32` | The UDP port synauson receives RTP on, for the SDP answer's m= line. RTCP is on `local_rtp_port` + 1. |

### SrtpConfig

SRTP keys (SDES, RFC 4568) for a SIP participant.

| Field | Number | Type | Description |
|---|---|---|---|
| `crypto_suite` | 1 | `string` | Crypto suite: "AES_CM_128_HMAC_SHA1_80", the only one supported. |
| `local_key` | 2 | `bytes` | Required. The 30-byte SRTP master key that encrypts what synauson sends (its a=crypto). |
| `remote_key` | 3 | `bytes` | Required. The peer's 30-byte SRTP master key, which decrypts what it sends (its a=crypto). |

### SipRemoteMedia

The media a SIP peer negotiated in its SDP.

| Field | Number | Type | Description |
|---|---|---|---|
| `remote_ip` | 1 | `string` | Required. The address the peer receives RTP on (its SDP c= line), as for `AddSipParticipantRequest.remote_ip`. |
| `remote_rtp_port` | 2 | `int32` | Required. Port the peer receives RTP on (its SDP m= line), 1 to 65535. RTCP goes to the next port. |
| `codec` | 3 | `string` | Required. The codec's RTP payload format name, as for `AddSipParticipantRequest.codec`. |
| `dtmf_payload_type` | 4 | `int32` | RFC 4733 telephone-event payload type; 0 turns RFC 4733 DTMF off, otherwise 96 to 127. |
| `remote_srtp_key` | 5 | optional `bytes` | The peer's 30-byte SRTP master key (its a=crypto), which decrypts what it sends. Required exactly when the reservation carried `local_srtp_key`. |

### ReserveSipParticipantRequest

Reserve a SIP participant's local RTP and RTCP ports before the peer's
media is known: the outbound call, whose SDP offer must carry our port
before the answer names the peer's. Both sockets are bound when this
returns, so media the peer sends early is queued, but nothing runs until
ConnectSipParticipant.

A reservation is not a participant: `GetConference` leaves it out. It
does hold its id and a place under the participant cap.
`RemoveParticipant` or `TerminateConference` releases it. Write-only:
nothing reads a reservation back.

Errors: `INVALID_ID`; `INVALID_ARGUMENT` (a key not 30 bytes, an
unsupported suite); `CONFERENCE_NOT_FOUND`; `PARTICIPANT_ALREADY_EXISTS`
(the id is a participant or already reserved); `RTP_PORTS_EXHAUSTED`;
`PARTICIPANT_LIMIT_REACHED`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The conference to join. |
| `participant_id` | 2 | `string` | Required. The new participant's id, chosen by the caller. |
| `local_srtp_key` | 3 | optional `bytes` | The 30-byte SRTP master key synauson encrypts with, advertised in the offer's a=crypto. Unset for plain RTP. |
| `srtp_crypto_suite` | 4 | `string` | Crypto suite of `local_srtp_key`: empty or "AES_CM_128_HMAC_SHA1_80", the only suite supported. |

### ReserveSipParticipantResponse

The ports are reserved.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The participant's id, as requested. |
| `local_rtp_port` | 2 | `int32` | Port for the SDP offer's m= line. |
| `local_rtcp_port` | 3 | `int32` | Always local_rtp_port + 1. |

### ConnectSipParticipantRequest

Start a participant reserved by `ReserveSipParticipant`, once the peer's
SDP answer is in. From then on it behaves as one added with
`AddSipParticipant`, sending from the port it receives on (symmetric RTP,
RFC 4961). Invalid arguments leave the reservation in place; any other
failure releases it, and the caller must reserve again. It never fails on
the participant cap: the reservation already holds its place.

Errors: `INVALID_ID`; `INVALID_ARGUMENT` (no `remote`, an empty or
malformed field, an unsupported codec, a port or DTMF payload type out of
range, a key not 30 bytes, SRTP on one side only);
`CONFERENCE_NOT_FOUND`; `SIP_RESERVATION_NOT_FOUND`;
`PARTICIPANT_ALREADY_EXISTS` (the id is a running participant: a
reservation connects once); `PARTICIPANT_START_FAILED`; `INTERNAL`; and
the detector errors (`DetectorConfig`).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The reservation's conference. |
| `participant_id` | 2 | `string` | Required. The reserved participant's id. |
| `remote` | 3 | [`SipRemoteMedia`](#sipremotemedia) | Required. The media the peer's SDP answer negotiated. |
| `detectors` | 4 | [`DetectorConfig`](#detectorconfig) | Detectors to run on the call's incoming audio. |

### ConnectSipParticipantResponse

The reserved participant is running.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The participant's id. |
| `local_rtp_port` | 2 | `int32` | The UDP port synauson receives RTP on, as reserved. |

### SendDtmfRequest

Send a DTMF digit to a SIP participant's peer: as RFC 4733
telephone-event packets when the participant has a DTMF payload type,
else as in-band audio tones.

Errors: `INVALID_ID`, `INVALID_ARGUMENT` (an invalid digit),
`CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND` (no SIP participant with
that id).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The SIP participant whose peer gets the digit. |
| `digit` | 3 | `string` | Required. One DTMF digit: "0" to "9", "*", "#", "A", "B", "C" or "D". |
| `duration_ms` | 4 | `int32` | How long the tone lasts, in ms (a duration); clamped to 70 to 500 (ITU-T Q.24). |

### SendDtmfResponse

The digit was sent.

### StreamDtmfEventsRequest

Subscribe to the DTMF digits a SIP participant's peer sends, from the
subscription on. Nothing is sent while no digit comes: the stream has no
heartbeat. A subscriber that falls behind gets `SUBSCRIBER_LAGGED` and
the stream ends: subscribe again.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND` (no
SIP participant with that id).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The SIP participant to listen to. |

### DtmfEvent

A DTMF digit the peer sent.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The SIP participant whose peer sent it. |
| `digit` | 2 | `string` | One digit: "0" to "9", "*", "#", "A" to "D". |
| `in_band` | 4 | `bool` | True when it was heard as an in-band tone in the audio; false when it came as an RFC 4733 telephone-event. |

### GetSipStatsRequest

Ask for a SIP participant's statistics.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND` (no
SIP participant with that id).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The SIP participant. |

### SipStats

A SIP participant's RTP receive statistics, named as RFC 3550 and the
W3C WebRTC statistics name them. All 0 until RTP arrives.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The SIP participant. |
| `packets_received` | 2 | `int64` | RTP packets received. |
| `packets_lost` | 3 | `int64` | RTP packets lost (RFC 3550's cumulative number of packets lost). |
| `avg_jitter_ns` | 4 | `int64` | Average interarrival jitter (RFC 3550), in ns. |
| `active_ssrc_count` | 6 | `int32` | Distinct RTP streams (SSRCs) of audio received so far. |

### GetSipStatsResponse

A SIP participant's statistics.

| Field | Number | Type | Description |
|---|---|---|---|
| `stats` | 1 | [`SipStats`](#sipstats) | The statistics now. |

## synauson/v1/webrtc.proto

### AddWebRtcParticipantRequest

Add a WebRTC peer (a browser, say) as a bidirectional participant. The
peer is the offerer: the caller relays its SDP offer here and forwards
synauson's answer back. Audio is Opus only; DTLS-SRTP, ICE and RTCP are
handled by synauson. Exchange ICE candidates with AddWebRtcIceCandidate
and StreamWebRtcIceCandidates.

Errors: `INVALID_ID`; `INVALID_ARGUMENT` (an invalid option, an
`sdp_offer` that is empty, isn't SDP, doesn't offer exactly one audio
media section, or can't be answered; no message or metadata contains
TURN credentials or the SDP);
`CONFERENCE_NOT_FOUND`; `PARTICIPANT_ALREADY_EXISTS`;
`PARTICIPANT_LIMIT_REACHED`; `LICENSE_REJECTED`, `LICENSE_DISCONNECTED`,
`LICENSE_EXPIRED` (the license starts nothing new); `INTERNAL`; and the
detector errors (`DetectorConfig`).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The conference to join. |
| `participant_id` | 2 | `string` | Required. The new participant's id, chosen by the caller. |
| `sdp_offer` | 3 | `string` | Required. The peer's SDP offer (from createOffer and setLocalDescription in a browser). |
| `detectors` | 4 | [`DetectorConfig`](#detectorconfig) | Detectors to run on the peer's audio. |
| `options` | 5 | [`WebRtcOptions`](#webrtcoptions) | Per-participant options. Anything left unset uses the server's defaults, then the built-in defaults documented per field. |

### WebRtcOptions

WebRTC options for one participant. Every field is optional; an unset
field inherits the server default. Invalid values fail
AddWebRtcParticipant with INVALID_ARGUMENT.

| Field | Number | Type | Description |
|---|---|---|---|
| `stun_server` | 1 | optional `string` | stun://host[:port] (the browser form stun:host is refused). An empty string turns STUN off for this participant. Default: the server's --webrtc-stun-server, which is off unless the operator sets one. |
| `turn_servers` | 2 | repeated `string` | turn(s)://user:password@host[:port][?transport=udp\|tcp]. Percent-encode any of : @ / ? # in the user or password. At most 8 relays; turn:// without a transport counts as two. Default: none. |
| `ice_transport_policy` | 3 | [`WebRtcIceTransportPolicy`](#webrtcicetransportpolicy) | Which ICE candidates to use. Default: ALL. |
| `ice_port_min` | 4 | optional `int32` | Lowest local port for the participant's ICE candidates, 1 to 65535; set both or neither. Default: the server's range, else any port. Each concurrent participant needs a port per local address (one for UDP and one for ICE-TCP), so size the range for the load. |
| `ice_port_max` | 5 | optional `int32` | Highest local port for the participant's ICE candidates; see ice_port_min. |
| `jitter_buffer_ms` | 6 | optional `int32` | Receive jitter buffer latency in ms (a duration), 0 to 2000. Default: the server's (200). Every mix of this participant's audio waits for it, so the others hear it late by the same amount. |
| `opus_bitrate_bps` | 7 | optional `int32` | Bitrate of the Opus audio synauson sends, in bits per second, 4000 to 650000. Default 64000. |
| `opus_dtx` | 8 | optional `bool` | Opus discontinuous transmission for the audio synauson sends: tiny packets during silence. Default true. |
| `opus_inband_fec` | 9 | optional `bool` | Opus in-band forward error correction for the audio synauson sends. Default false. |
| `opus_packet_loss_percentage` | 10 | optional `int32` | Expected packet loss, 0 to 100, which sizes the in-band FEC. Default 10 when opus_inband_fec is on, else 0 (FEC adds nothing at 0). |

### WebRtcEffectiveOptions

The options a live participant runs with. The ICE port range, jitter
buffer and Opus fields are read back from its live media; the STUN, TURN
and policy fields are the resolved values synauson applied.

| Field | Number | Type | Description |
|---|---|---|---|
| `stun_server` | 1 | `string` | The STUN server; empty when STUN is off. |
| `turn_servers` | 2 | repeated `string` | The TURN servers, credentials redacted: turn://***@host:port. |
| `ice_transport_policy` | 3 | [`WebRtcIceTransportPolicy`](#webrtcicetransportpolicy) | The ICE transport policy in force. |
| `ice_port_min` | 4 | optional `int32` | Lowest local ICE port; unset when the ICE agent may pick any port. |
| `ice_port_max` | 5 | optional `int32` | Highest local ICE port; unset when the ICE agent may pick any port. |
| `jitter_buffer_ms` | 6 | `int32` | Receive jitter buffer latency in ms (a duration), from the live jitter buffer once RTP has arrived. |
| `opus_bitrate_bps` | 7 | `int32` | Bitrate of the Opus audio synauson sends, in bits per second. |
| `opus_dtx` | 8 | `bool` | Whether Opus discontinuous transmission is on. |
| `opus_inband_fec` | 9 | `bool` | Whether Opus in-band forward error correction is on. |
| `opus_packet_loss_percentage` | 10 | `int32` | The expected packet loss the FEC is sized for, 0 to 100. |

### AddWebRtcParticipantResponse

The WebRTC participant was added.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The participant's id, as requested. |
| `sdp_answer` | 2 | `string` | Synauson's SDP answer, already applied on synauson's side. Forward it to the peer (setRemoteDescription in a browser). |

### AddWebRtcIceCandidateRequest

Pass one of the peer's ICE candidates to synauson (trickle ICE): call it
for each candidate the peer finds (a browser's icecandidate event).

Errors: `INVALID_ID`, `INVALID_ARGUMENT` (an empty `candidate`),
`CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND`.

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The WebRTC participant the candidate is for. |
| `candidate` | 3 | `string` | Required. The candidate's a=candidate:... line. |
| `sdp_mline_index` | 4 | `int32` | The index of the SDP media section it belongs to. |

### AddWebRtcIceCandidateResponse

The candidate was added.

### StreamWebRtcIceCandidatesRequest

Subscribe to synauson's ICE candidates for a WebRTC participant: those
found before the subscription, then new ones as they are found. Forward
each to the peer (addIceCandidate in a browser). The stream sends nothing
between candidates (no heartbeat) and stays open after
`end_of_candidates` until the participant goes. A subscriber that falls
behind gets `SUBSCRIBER_LAGGED` and the stream ends: subscribe again.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND` (no
WebRTC participant with that id).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The WebRTC participant whose candidates to stream. |

### WebRtcIceCandidate

One of synauson's ICE candidates, or the end of them.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The WebRTC participant it is for. |
| `candidate` | 2 | `string` | The candidate's a=candidate:... line; empty with end_of_candidates. |
| `sdp_mline_index` | 3 | `int32` | The index of the SDP media section it belongs to. |
| `end_of_candidates` | 4 | `bool` | True when ICE gathering is complete; candidate is then empty. |

### GetWebRtcStatsRequest

Ask for a WebRTC participant's statistics.

Errors: `INVALID_ID`, `CONFERENCE_NOT_FOUND`, `PARTICIPANT_NOT_FOUND` (no
WebRTC participant with that id).

| Field | Number | Type | Description |
|---|---|---|---|
| `conference_id` | 1 | `string` | Required. The participant's conference. |
| `participant_id` | 2 | `string` | Required. The WebRTC participant. |

### WebRtcStats

A WebRTC participant's connection state, its RTP counters and the
options it runs with. The counters come from the WebRTC statistics: a
counter it can't report yet is 0.

| Field | Number | Type | Description |
|---|---|---|---|
| `participant_id` | 1 | `string` | The WebRTC participant. |
| `ice_connection_state` | 2 | `string` | The ICE connection state, as WebRTC names it (RTCIceConnectionState): "new", "checking", "connected", "completed", "failed", "disconnected" or "closed". Others may be added. |
| `connection_state` | 3 | `string` | The peer connection state, combining ICE and DTLS, as WebRTC names it (RTCPeerConnectionState): "new", "connecting", "connected", "disconnected", "failed" or "closed". Others may be added. |
| `packets_received` | 4 | `int64` | RTP packets received, over every stream the peer sends. |
| `packets_lost` | 5 | `int64` | RTP packets lost, as the receive jitter buffer counts them. |
| `packets_sent` | 6 | `int64` | RTP packets synauson sent. With nothing routed to the participant, synauson may send none, so this stays 0 until a route carries audio. |
| `bytes_received` | 7 | `int64` | Bytes of RTP received. |
| `bytes_sent` | 8 | `int64` | Bytes of RTP sent. |
| `max_jitter_ns` | 9 | `int64` | The largest receive interarrival jitter of the streams the peer sends, in ns (`SipStats.avg_jitter_ns` is an average). |
| `rtt_ms` | 10 | `int64` | Round-trip time in ms (a duration), once the peer's first RTCP receiver report has arrived; 0 before, and under 0.5 ms rounds to 0. |
| `effective_options` | 11 | [`WebRtcEffectiveOptions`](#webrtceffectiveoptions) | The options the participant runs with. |

### GetWebRtcStatsResponse

A WebRTC participant's statistics.

| Field | Number | Type | Description |
|---|---|---|---|
| `stats` | 1 | [`WebRtcStats`](#webrtcstats) | The statistics now. |

### WebRtcIceTransportPolicy

Which ICE candidates a participant may use. May gain values: accept ones
you don't know in `WebRtcEffectiveOptions`.

| Value | Number | Description |
|---|---|---|
| `WEB_RTC_ICE_TRANSPORT_POLICY_UNSPECIFIED` | 0 | Unset: inherit (the built-in default is ALL). |
| `WEB_RTC_ICE_TRANSPORT_POLICY_ALL` | 1 | Host, server-reflexive and relayed candidates. |
| `WEB_RTC_ICE_TRANSPORT_POLICY_RELAY` | 2 | Relayed (TURN) candidates only; synauson's own addresses are never sent to the peer, and STUN is skipped. Needs at least one TURN server. |
