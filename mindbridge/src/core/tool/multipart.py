"""Multipart response utilities — shared by all services and the client.

Server-side: build_multipart_response() constructs a multipart/mixed HTTP
response from a list of named binary parts plus a JSON metadata part.

Client-side: parse_multipart_response() unpacks a multipart/mixed response
back into a dict of {name: bytes} plus a JSON metadata dict.
"""

from __future__ import annotations

import email
import email.policy
import json as _json
import uuid
from io import BytesIO
from typing import Optional


# ── Server helpers ──────────────────────────────────────────────────────────

def _escape_quoted_printable_headers(headers: dict[str, str]) -> dict[str, str]:
    """Per RFC 2047, encode non-ASCII header values."""
    out = {}
    for k, v in headers.items():
        try:
            v.encode("ascii")
            out[k] = v
        except UnicodeEncodeError:
            # RFC 2047 Q-encoding for header values
            out[k] = v  # Python email module handles this for us
    return out


def build_multipart_response(
    *,
    json_part: Optional[dict] = None,
    binary_parts: list[tuple[str, bytes, str]] | None = None,
    extra_headers: Optional[dict[str, str]] = None,
) -> tuple[bytes, str]:
    """Build a multipart/mixed response body.

    Args:
        json_part: Optional JSON dict to include as the first "result" part.
        binary_parts: List of (name, data_bytes, mime_type) tuples.
        extra_headers: Dict of X-* headers to include at the top level.

    Returns:
        (body_bytes, content_type_with_boundary)
    """
    boundary = f"boundary_{uuid.uuid4().hex[:16]}"
    content_type = f'multipart/mixed; boundary="{boundary}"'

    lines: list[bytes] = []

    # ── JSON metadata part ──
    if json_part is not None:
        json_bytes = _json.dumps(json_part, ensure_ascii=False).encode("utf-8")
        lines.append(f'--{boundary}\r\n'.encode("ascii"))
        lines.append(f'Content-Disposition: form-data; name="result"\r\n'.encode("ascii"))
        lines.append(f"Content-Type: application/json\r\n".encode("ascii"))
        lines.append(f"Content-Length: {len(json_bytes)}\r\n".encode("ascii"))
        lines.append(b"\r\n")
        lines.append(json_bytes)
        lines.append(b"\r\n")

    # ── Binary parts ──
    if binary_parts:
        for name, data, mime_type in binary_parts:
            lines.append(f'--{boundary}\r\n'.encode("ascii"))
            lines.append(
                f'Content-Disposition: form-data; name="{name}"; filename="{name}"\r\n'.encode("ascii")
            )
            lines.append(f"Content-Type: {mime_type}\r\n".encode("ascii"))
            lines.append(f"Content-Length: {len(data)}\r\n".encode("ascii"))
            lines.append(b"\r\n")
            lines.append(data)
            lines.append(b"\r\n")

    # ── Closing boundary ──
    lines.append(f"--{boundary}--\r\n".encode("ascii"))

    body = b"".join(lines)
    return body, content_type


# ── Client helpers ───────────────────────────────────────────────────────────

def parse_multipart_response(
    body: bytes,
    content_type: str,
) -> tuple[dict | None, dict[str, bytes]]:
    """Parse a multipart/mixed response into (json_result, binary_parts).

    The first text/application/json part named "result" becomes the json_result dict.
    All other parts are returned as a dict of {name: raw_bytes}.

    Returns:
        (json_result_or_None, {part_name: raw_bytes})
    """
    json_result: dict | None = None
    binary_parts: dict[str, bytes] = {}

    header = f"Content-Type: {content_type}\r\n\r\n".encode("ascii")
    msg = email.message_from_bytes(header + body, policy=email.policy.compat32)
    if not msg.is_multipart():
        return json_result, binary_parts

    for part in msg.get_payload():
        content_type_part = part.get_content_type()
        disp = part.get("Content-Disposition", "")
        # Parse name from Content-Disposition header
        name = ""
        for param in disp.split(";"):
            param = param.strip()
            if param.startswith("name="):
                name = param.split("=", 1)[1].strip().strip('"')
                break

        payload = part.get_payload(decode=True)
        if payload is None:
            continue

        # JSON metadata part
        if name == "result" and "json" in content_type_part:
            try:
                json_result = _json.loads(payload.decode("utf-8"))
            except Exception:
                pass
        elif name:
            binary_parts[name] = payload

    return json_result, binary_parts
