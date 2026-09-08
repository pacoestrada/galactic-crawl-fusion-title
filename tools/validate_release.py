#!/usr/bin/env python3
"""Validate the distribution; this does not render or instantiate Fusion nodes."""
from __future__ import annotations
import ctypes
import ctypes.util
import hashlib
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/Galactic Crawl.setting'
ASSETS = ('Galactic-Crawl.drfx', 'Galactic-Crawl.setting', 'Galactic-Crawl-quickstart-es.txt')
MEMBER = 'Edit/Titles/Galactic Crawl.setting'


def check_lua(source: bytes) -> None:
    library = ctypes.util.find_library('lua5.4')
    if not library:
        raise RuntimeError('Lua 5.4 shared library required (Debian/Ubuntu: liblua5.4-0)')
    lua = ctypes.CDLL(library)
    lua.luaL_newstate.restype = ctypes.c_void_p
    lua.luaL_openlibs.argtypes = [ctypes.c_void_p]
    lua.luaL_loadbufferx.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_char_p]
    lua.luaL_loadbufferx.restype = ctypes.c_int
    lua.lua_pcallk.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_ssize_t, ctypes.c_void_p]
    lua.lua_pcallk.restype = ctypes.c_int
    lua.lua_tolstring.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
    lua.lua_tolstring.restype = ctypes.c_char_p
    lua.lua_close.argtypes = [ctypes.c_void_p]
    constructors = ('GroupOperator', 'InstanceInput', 'InstanceOutput', 'GroupInfo', 'OperatorInfo', 'Background', 'TextPlus', 'Custom', 'Merge', 'Input')
    prelude = 'function ordered() return function(t) return t end end\n'
    for name in constructors:
        prelude += f'function {name}(t) t.__kind="{name}"; return t end\n'
    checks = r'''
assert(setting.ActiveTool == 'GalacticCrawl', 'unexpected active tool')
local group = assert(setting.Tools.GalacticCrawl, 'missing macro')
local tools = group.Tools
local expected = {Canvas='Background', Space='Background', Story='TextPlus', Stars='Custom', Crawl='Custom', Ink='Background', Final='Merge'}
local count = 0
for name,node in pairs(tools) do
  assert(expected[name] == node.__kind, 'unexpected node: '..name)
  count = count + 1
end
assert(count == 7, 'unexpected node count')
local controls = 0
for name,control in pairs(group.Inputs) do
  local target = assert(tools[control.SourceOp], 'unresolved control: '..name)
  assert(target.Inputs[control.Source], 'missing published input: '..name)
  controls = controls + 1
end
assert(controls == 23, 'unexpected published component count')
local visiting, visited = {}, {}
local function visit(name)
  assert(not visiting[name], 'node cycle at '..name)
  if visited[name] then return end
  visiting[name] = true
  for key,value in pairs(tools[name].Inputs) do
    if type(value) == 'table' and value.SourceOp then
      assert(tools[value.SourceOp], 'unresolved reference: '..name..'.'..key)
      assert(value.Source == 'Output', 'unexpected output socket')
      visit(value.SourceOp)
    end
  end
  visiting[name] = nil
  visited[name] = true
end
for name in pairs(tools) do visit(name) end
assert(group.Outputs.MainOutput1.SourceOp == 'Final')
assert(group.Outputs.MainOutput1.Source == 'Output')
assert(tools.Story.Inputs.UseFrameFormatSettings.Value == 0)
assert(tools.Story.Inputs.Width.Value == 1920 and tools.Story.Inputs.Height.Value == 4096)
assert(tools.Crawl.Inputs.Image1.SourceOp == 'Canvas' and tools.Crawl.Inputs.Image2.SourceOp == 'Story')
assert(tools.Final.Inputs.Background.SourceOp == 'Stars' and tools.Final.Inputs.Foreground.SourceOp == 'Ink')
assert(tools.Stars.Inputs.NumberIn5.Value == 1)
for _,name in ipairs({'Stars','Crawl'}) do
  for _,channel in ipairs({'Red','Green','Blue','Alpha'}) do
    assert(type(tools[name].Inputs[channel..'Expression'].Value) == 'string')
  end
end
'''
    code = prelude.encode() + b'local setting = ' + source + b'\n' + checks.encode()
    state = lua.luaL_newstate()
    if not state:
        raise RuntimeError('Cannot create Lua parser state')
    try:
        lua.luaL_openlibs(state)
        result = lua.luaL_loadbufferx(state, code, len(code), b'Galactic Crawl.setting', b't')
        if not result:
            result = lua.lua_pcallk(state, 0, 0, 0, 0, None)
        if result:
            raise ValueError(lua.lua_tolstring(state, -1, None).decode())
    finally:
        lua.lua_close(state)


def check_links() -> None:
    for doc in ROOT.rglob('*.md'):
        if '.git' in doc.parts:
            continue
        for target in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
            target = target.strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = (doc.parent / unquote(parsed.path)).resolve()
            if not path.is_relative_to(ROOT) or not path.exists():
                raise ValueError(f'Broken local link in {doc.relative_to(ROOT)}: {target}')


def main() -> None:
    source = SOURCE.read_bytes()
    source.decode('utf-8')
    check_lua(source)
    assert (ROOT / 'dist/Galactic-Crawl.setting').read_bytes() == source, 'standalone setting mismatch'
    with zipfile.ZipFile(ROOT / 'dist/Galactic-Crawl.drfx') as z:
        assert z.namelist() == [MEMBER], 'unexpected archive entries or duplicate members'
        assert z.testzip() is None, 'corrupt ZIP member'
        assert z.read(MEMBER) == source, 'bundled setting mismatch'
    lines = (ROOT / 'dist/SHA256SUMS.txt').read_text().splitlines()
    expected = {name: hashlib.sha256((ROOT / 'dist' / name).read_bytes()).hexdigest() for name in ASSETS}
    assert len(lines) == len(expected), 'unexpected checksum line count'
    for line in lines:
        digest, name = line.split('  ', 1)
        assert expected.pop(name) == digest, f'checksum mismatch: {name}'
    assert not expected, 'missing checksums'
    check_links()
    print('OK: Lua syntax/table evaluation; 7 nodes and 23 published components; acyclic, resolved graph')
    print('OK: DRFX integrity and paths; both settings match; 3 SHA-256 checksums; local Markdown links')
    print('Scope: structural validation only. This script does not test Resolve installation or rendering.')

if __name__ == '__main__':
    main()
