import logging

import pytest


@pytest.mark.asyncio
async def test_client(caplog):
    caplog.set_level(logging.DEBUG)
    from synthpy import Synth

    synth = Synth("localhost:8182")

    await synth.ingest.put_documents(
        "my_namespace", "my_collection", document={"user": "damien", "login": 2}
    )

    await synth.ingest.put_documents(
        "my_namespace", "my_collection", document={"user": "damien_alt", "login": 1}
    )

    await synth.override.optionalise("my_namespace", "my_collection.login")

    override = {"number": {"u64range": {"low": 0, "high": 1000, "step": 1}}}

    await synth.override.put_override(
        "my_namespace", field="my_collection.login", override=override
    )

    res = await synth.generate.get_documents("my_namespace", size=10)
    print(res)

    namespaces = await synth.namespace.get_namespaces()
    assert "my_namespace" in namespaces

    await synth.namespace.get_schema("my_namespace", "my_collection")

    await synth.namespace.rollback_namespace("my_namespace", 1)

    gen_1 = await synth.namespace.get_schema("my_namespace", generation=1)
    gen_latest = await synth.namespace.get_schema("my_namespace")
    assert gen_1 == gen_latest

    await synth.namespace.delete_collection("my_namespace", "my_collection")

    await synth.namespace.delete_namespace("my_namespace", erase=True)

    raise NotImplementedError
