from ncclient import manager

with manager.connect(
    host="localhost", port=830,
    username="netconf", password="netconf",
    hostkey_verify=False, allow_agent=False, look_for_keys=False,
) as m:
    print("session-id:", m.session_id)
    resposta = m.get_config(source="running")
    with open("rpc-reply.xml", "w", encoding="utf-8") as f:
        f.write(resposta.xml)
    print("salvo rpc-reply.xml")