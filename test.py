from paestro.utils import Paestro

cmd = 'hostnamectl'
cmd = f'PS1="" bash -ic "{cmd}"'
result, lines, ms = Paestro.ssh_exec(cmd, '192.168.0.110', '--', '--', pty=True)
print(result)
print(repr(result))

plain_text, formats = Paestro.parse_ansi_modifiers(result)
print(plain_text)
print(formats)