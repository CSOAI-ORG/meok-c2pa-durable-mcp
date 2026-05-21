"""Smoke tests for meok-c2pa-durable-mcp."""
import sys, os, inspect, traceback, hashlib, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    build_durable_manifest,
    build_soft_binding,
    merge_hard_and_soft,
    verify_durable_manifest,
    list_soft_binding_methods,
    sign_cose1_envelope,
    SOFT_BINDING_METHODS,
    C2PA_VERSION,
)


SAMPLE_HASH = hashlib.sha256(b"sample image").hexdigest()


def test_build_durable_manifest_returns_manifest():
    r = build_durable_manifest(SAMPLE_HASH, "image/png", model_id="claude-opus-4.7")
    assert r["manifest"]["c2pa_version"] == C2PA_VERSION
    assert r["manifest"]["format"] == "image/png"
    assert len(r["manifest"]["assertions"]) >= 2


def test_build_durable_manifest_has_hard_binding():
    r = build_durable_manifest(SAMPLE_HASH, "image/jpeg")
    hard_assertions = [a for a in r["manifest"]["assertions"] if a["label"] == "c2pa.hash.data"]
    assert len(hard_assertions) == 1
    assert hard_assertions[0]["data"]["hash"] == SAMPLE_HASH


def test_build_soft_binding_default():
    r = build_soft_binding({"content_hash": SAMPLE_HASH, "width": 1024, "height": 1024})
    assert r["soft_binding_assertion"]["label"] == "c2pa.soft_binding.v2"
    assert "Digimarc" in r["method_details"]["label"]


def test_build_soft_binding_unsupported():
    r = build_soft_binding({"content_hash": SAMPLE_HASH}, "fake_method")
    assert "error" in r


def test_merge_hard_and_soft_extends_assertions():
    m = build_durable_manifest(SAMPLE_HASH, "image/png")
    sb = build_soft_binding({"content_hash": SAMPLE_HASH, "width": 512, "height": 512})
    merged = merge_hard_and_soft(m["manifest"], sb["soft_binding_assertion"])
    assert merged["durable_manifest"]["durable"] is True
    assert len(merged["durable_manifest"]["assertions"]) == 3
    assert "signature" in merged["durable_manifest"]


def test_verify_durable_manifest_round_trip():
    asset_meta = {"content_hash": SAMPLE_HASH, "width": 1024, "height": 1024}
    m = build_durable_manifest(SAMPLE_HASH, "image/png")
    sb = build_soft_binding(asset_meta)
    merged = merge_hard_and_soft(m["manifest"], sb["soft_binding_assertion"])
    v = verify_durable_manifest(asset_meta, merged["durable_manifest"])
    assert v["valid"] is True
    assert v["hard_binding_ok"] is True
    assert v["soft_binding_ok"] is True


def test_verify_detects_hard_binding_break():
    asset_meta = {"content_hash": "tampered_hash", "width": 1024, "height": 1024}
    m = build_durable_manifest(SAMPLE_HASH, "image/png")
    sb = build_soft_binding({"content_hash": SAMPLE_HASH, "width": 1024, "height": 1024})
    merged = merge_hard_and_soft(m["manifest"], sb["soft_binding_assertion"])
    v = verify_durable_manifest(asset_meta, merged["durable_manifest"])
    assert v["hard_binding_ok"] is False


def test_list_methods_returns_three():
    r = list_soft_binding_methods()
    assert r["count"] == 3
    assert "digimarc_soft" in r["methods"]


def test_sign_cose1_envelope_emits_signature():
    m = build_durable_manifest(SAMPLE_HASH, "image/png")
    r = sign_cose1_envelope(m["manifest"])
    assert "signature" in r
    assert r["kid"] == "meok-default"


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    p = f = 0
    for fn in fns:
        try:
            fn(); print(f"OK {fn.__name__}"); p += 1
        except Exception as e:
            print(f"X  {fn.__name__}: {type(e).__name__}: {e}"); traceback.print_exc(); f += 1
    print(f"\n{p} passed, {f} failed")
