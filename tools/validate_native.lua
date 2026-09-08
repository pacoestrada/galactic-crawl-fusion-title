local path=arg[1]
local f=assert(io.open(path,'rb')); local src=f:read('*a'); f:close()
assert(loadstring('return '..src,'@'..path))
local s=assert(bmd.readfile(path)); local g=assert(s.Tools.GalacticCrawl)
assert(s.ActiveTool=='GalacticCrawl')
local count=0
for k,v in pairs(g.Tools) do if type(v)=="table" then count=count+1 end end
assert(count==7)
for k,v in pairs(g.Inputs) do if type(v)=='table' then assert(g.Tools[v.SourceOp], k..' source missing') end end
assert(g.Tools.Story.Inputs.UseFrameFormatSettings.Value==0)
assert(g.Tools.Story.Inputs.Height.Value==4096)
assert(g.Tools.Crawl.Inputs.Image2.SourceOp=='Story')
assert(g.Tools.Stars.Inputs.NumberIn5.Value==1)
print('OK: native Fusion Lua parse and bmd.readfile; 7 nodes; Inspector references resolved.')
