#!/usr/bin/env python3
"""Write the API reference (docs/api.md) from the protos' comments.

    gen_api_docs.py <descriptor set> > docs/api.md

The descriptor set must carry source info (the comments). Either form works:

    buf build -o api.json                        # JSON, needs nothing else
    python -m grpc_tools.protoc -I. --include_source_info \\
        --descriptor_set_out=api.binpb synauson/v1/*.proto   # binary, needs protobuf

Both give the same output. Only the standard library is needed for JSON.
"""
import json
import pathlib
import re
import sys

# FileDescriptorProto, DescriptorProto, EnumDescriptorProto and
# ServiceDescriptorProto field numbers, as source info paths use them.
FILE_MESSAGE, FILE_ENUM, FILE_SERVICE = 4, 5, 6
MSG_FIELD, MSG_NESTED, MSG_ENUM, MSG_ONEOF = 2, 3, 4, 8
ENUM_VALUE = 2
SERVICE_METHOD = 2

SCALARS = {
    "TYPE_DOUBLE": "double", "TYPE_FLOAT": "float", "TYPE_INT64": "int64",
    "TYPE_UINT64": "uint64", "TYPE_INT32": "int32", "TYPE_FIXED64": "fixed64",
    "TYPE_FIXED32": "fixed32", "TYPE_BOOL": "bool", "TYPE_STRING": "string",
    "TYPE_BYTES": "bytes", "TYPE_UINT32": "uint32", "TYPE_SFIXED32": "sfixed32",
    "TYPE_SFIXED64": "sfixed64", "TYPE_SINT32": "sint32", "TYPE_SINT64": "sint64",
}


def load(path):
    data = pathlib.Path(path).read_bytes()
    if path.endswith(".json"):
        return json.loads(data)
    from google.protobuf import descriptor_pb2, json_format

    fds = descriptor_pb2.FileDescriptorSet.FromString(data)
    return json_format.MessageToDict(fds)


def comments(file):
    """Leading comments keyed by source path."""
    out = {}
    for loc in file.get("sourceCodeInfo", {}).get("location", []):
        text = loc.get("leadingComments")
        if text:
            out[tuple(int(p) for p in loc["path"])] = clean(text)
    return out


def clean(text):
    lines = [line[1:] if line.startswith(" ") else line for line in text.split("\n")]
    return "\n".join(lines).strip("\n")


def anchor(name):
    return "#" + re.sub(r"[^a-z0-9_-]", "", name.lower())


def short(type_name, package):
    name = type_name.lstrip(".")
    prefix = package + "."
    return name[len(prefix):] if name.startswith(prefix) else name


def link(type_name, package):
    name = short(type_name, package)
    if "." in name:
        return f"`{name}`"
    return f"[`{name}`]({anchor(name)})"


def cell(text):
    """A comment as one markdown table cell."""
    if not text:
        return ""
    out = []
    for para in text.split("\n\n"):
        lines = para.split("\n")
        joined = ""
        for line in lines:
            if line.startswith("- ") and joined:
                joined += "<br>" + line
            elif joined:
                joined += " " + line.strip()
            else:
                joined = line
        out.append(joined)
    return "<br><br>".join(out).replace("|", "\\|")


def field_type(field, package, maps):
    if field.get("type") == "TYPE_MESSAGE" and field["typeName"] in maps:
        key, value = maps[field["typeName"]]
        return f"map<{field_type(key, package, maps)}, {field_type(value, package, maps)}>"
    if field.get("type") in ("TYPE_MESSAGE", "TYPE_ENUM"):
        return link(field["typeName"], package)
    return f"`{SCALARS[field['type']]}`"


def render(fds):
    # buf's image also carries the imports (google/protobuf/...), protoc's set
    # only the files named, so keep just the API's own files.
    files = sorted((f for f in fds["file"] if f["name"].startswith("synauson/")),
                   key=lambda f: f["name"])
    package = files[0]["package"]
    out = [
        "# synauson API reference",
        "",
        f"Package `{package}`. Generated from the comments in `synauson/v1/*.proto` by",
        "`tools/gen_api_docs.py`; edit the protos, not this file.",
        "",
    ]

    # Map entry messages, by full name, so map fields print as map<K, V>.
    maps = {}

    def collect(prefix, messages):
        for m in messages:
            full = f"{prefix}.{m['name']}"
            if m.get("options", {}).get("mapEntry"):
                key, value = sorted(m["field"], key=lambda f: f["number"])
                maps[full] = (key, value)
            collect(full, m.get("nestedType", []))

    for f in files:
        collect("." + f["package"], f.get("messageType", []))

    services = [(f, si, svc) for f in files for si, svc in enumerate(f.get("service", []))]
    for f, si, service in sorted(services, key=lambda x: x[2]["name"]):
        docs = comments(f)
        out += [f"## Service `{service['name']}`", ""]
        text = docs.get((FILE_SERVICE, si))
        if text:
            out += [text, ""]
        for mi, method in enumerate(service.get("method", [])):
            streaming = "stream " if method.get("serverStreaming") else ""
            client = "stream " if method.get("clientStreaming") else ""
            out += [
                f"### {method['name']}",
                "",
                f"`rpc {method['name']}({client}{short(method['inputType'], package)})"
                f" returns ({streaming}{short(method['outputType'], package)})`",
                "",
                f"Request: {link(method['inputType'], package)}."
                f" Response: {'a stream of ' if streaming else ''}"
                f"{link(method['outputType'], package)}.",
                "",
            ]
            text = docs.get((FILE_SERVICE, si, SERVICE_METHOD, mi))
            if text:
                out += [text, ""]

    for f in files:
        if not f.get("messageType") and not f.get("enumType"):
            continue
        docs = comments(f)
        out += [f"## {f['name']}", ""]
        for i, m in enumerate(f.get("messageType", [])):
            out += render_message(m, (FILE_MESSAGE, i), docs, package, maps)
        for i, e in enumerate(f.get("enumType", [])):
            out += render_enum(e, (FILE_ENUM, i), docs)
    return "\n".join(out).rstrip("\n") + "\n"


def render_message(m, path, docs, package, maps, prefix=""):
    if m.get("options", {}).get("mapEntry"):
        return []
    name = prefix + m["name"]
    out = [f"### {name}", ""]
    text = docs.get(path)
    if text:
        out += [text, ""]
    fields = m.get("field", [])
    oneofs = m.get("oneofDecl", [])
    if fields:
        out += ["| Field | Number | Type | Description |", "|---|---|---|---|"]
        for i, field in enumerate(fields):
            label = ""
            if field.get("label") == "LABEL_REPEATED" and field.get("typeName") not in maps:
                label = "repeated "
            elif field.get("proto3Optional"):
                label = "optional "
            elif "oneofIndex" in field:
                label = f"oneof {oneofs[field['oneofIndex']]['name']}: "
            description = cell(docs.get(path + (MSG_FIELD, i)))
            if field.get("options", {}).get("deprecated"):
                description = ("Deprecated. " + description).strip()
            out.append(
                f"| `{field['name']}` | {field['number']} | {label}{field_type(field, package, maps)} | {description} |"
            )
        out.append("")
    for i, oneof in enumerate(oneofs):
        if all(f.get("proto3Optional") for f in fields if f.get("oneofIndex") == i):
            continue
        text = docs.get(path + (MSG_ONEOF, i))
        if text:
            out += [f"`oneof {oneof['name']}`: {cell(text)}", ""]
    reserved = [r for r in m.get("reservedRange", [])]
    names = m.get("reservedName", [])
    if reserved or names:
        numbers = []
        for r in reserved:
            start, end = int(r["start"]), int(r["end"]) - 1
            numbers.append(str(start) if start == end else f"{start}-{end}")
        parts = []
        if numbers:
            single = len(numbers) == 1 and "-" not in numbers[0]
            parts.append(("number " if single else "numbers ") + ", ".join(numbers))
        if names:
            parts.append("names " + ", ".join(f"`{n}`" for n in names))
        out += [f"Reserved (removed, never reused): {'; '.join(parts)}.", ""]
    for i, nested in enumerate(m.get("nestedType", [])):
        out += render_message(nested, path + (MSG_NESTED, i), docs, package, maps, name + ".")
    for i, e in enumerate(m.get("enumType", [])):
        out += render_enum(e, path + (MSG_ENUM, i), docs, name + ".")
    return out


def render_enum(e, path, docs, prefix=""):
    out = [f"### {prefix}{e['name']}", ""]
    text = docs.get(path)
    if text:
        out += [text, ""]
    out += ["| Value | Number | Description |", "|---|---|---|"]
    for i, value in enumerate(e.get("value", [])):
        out.append(
            f"| `{value['name']}` | {value.get('number', 0)} | {cell(docs.get(path + (ENUM_VALUE, i)))} |"
        )
    out.append("")
    return out


def main(argv):
    if len(argv) != 2:
        sys.exit(__doc__)
    sys.stdout.write(render(load(argv[1])))


if __name__ == "__main__":
    main(sys.argv)
