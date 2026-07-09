import math
from types import SimpleNamespace as NS

from pipeline.engines import extract_p_agree


def resp(toks):
    top = [NS(token=t, logprob=math.log(p)) for t, p in toks]
    pos0 = NS(token=toks[0][0], logprob=math.log(toks[0][1]), top_logprobs=top)
    return NS(choices=[NS(logprobs=NS(content=[pos0]))])


def test_token_variants_pool_correctly():
    r = resp([(" A", 0.6), ("a", 0.2), ("A.", 0.1), ("D", 0.05)])
    p, anom = extract_p_agree(r)
    assert not anom
    want = (0.9 + 1e-6) / (0.95 + 2e-6)
    assert abs(p - want) < 1e-9


def test_d_variants_and_verdict_side():
    r = resp([(" D", 0.7), ("d", 0.2), ("A", 0.05)])
    p, anom = extract_p_agree(r)
    assert not anom
    assert p < 0.5


def test_missing_d_mass():
    p, anom = extract_p_agree(resp([("A", 0.99)]))
    assert not anom
    assert p > 0.99


def test_anomaly_no_a_or_d():
    p, anom = extract_p_agree(resp([("Yes", 0.7), ("No", 0.3)]))
    assert anom
    assert p == 0.5


def test_anomaly_empty_content():
    r = NS(choices=[NS(logprobs=NS(content=[]))])
    assert extract_p_agree(r) == (0.5, True)
