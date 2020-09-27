--[[
This is the native export script for Shakersynth.

Place this script in your "Scripts" folder like:

   c:\Users\Jarpy\Saved Games\DCS.openbeta\Scripts\Shakersynth.lua

and add this line to "Export.lua" in the same folder:

   dofile(require('lfs').writedir()..'Scripts/Shakersynth.lua')
]]--

function LuaExportStart()
   local lua_socket_dir = lfs.currentdir().."/LuaSocket/"
   package.path  = package.path  .. ";" .. lua_socket_dir .. "?.lua"
   package.cpath = package.cpath .. ";" .. lua_socket_dir .. "?.dll"

   socket = require("socket")
   shksynsocket = socket.try(socket.udp())
   socket.try(shksynsocket:settimeout(.001))
   socket.try(shksynsocket:setpeername("127.0.0.1", 17707))
end

function LuaExportBeforeNextFrame()
end

function LuaExportAfterNextFrame()
   local aircraft = LoGetSelfData()
   local module = aircraft.Name
   local main_panel = GetDevice(0)

   -- Read rotor RPM percentage from the gauge.
   local rotor_rpm_percent = 0
   if module == "Mi-8MT" then
      rotor_rpm_percent = main_panel:get_argument_value(42) * 100
      rotor_pitch       = main_panel:get_argument_value(36)
   elseif module == "UH-1H" then
      rotor_rpm_percent = main_panel:get_argument_value(123) * 100
      rotor_pitch       = 1 -- Not available in Huey.
   else
      -- Unsupported helicopter or not a helicopter.
      rotor_rpm_percent = 0
      rotor_pitch       = 0
   end

   local payload = string.format(
      "---\n" ..
      "module: %s\n" ..
      "rotor_rpm_percent: %.16f\n" ..
      "rotor_pitch: %.16f\n",
      module,
      rotor_rpm_percent,
      rotor_pitch
   )

   socket.try(shksynsocket:send(payload))
end

function LuaExportStop()
   socket.try(shksynsocket:send("{}"))
   shksynsocket:close()
end

function LuaExportActivityNextEvent(t)
end
