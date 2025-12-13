import marshal, base64

with open("tite.py", "r") as f:
    source = f.read()

code = compile(source, "<string>", "exec")
marshaled = marshal.dumps(code)
encoded = base64.b64encode(marshaled).decode()

with open("tite.py", "w") as f:
    f.write('import marshal, base64\n')
    f.write(f'code = base64.b64decode("""{encoded}""")\n')
    f.write('exec(marshal.loads(code))\n')
