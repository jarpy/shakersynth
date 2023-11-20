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

   if not aircraft then
      return
   end

   local module = aircraft.Name
   local main_panel = GetDevice(0)

   -- Read rotor RPM percentage from the gauge #TODO: use loEngineInfo()?
   local rotor_rpm_percent = 0
   local doors = "0"  -- array of open doors (float)
   local ammo = "0" -- string that will be sent [%s] as a yaml array

   if module == "Mi-8MT" or module == "Mi-24P" then
      rotor_rpm_percent = main_panel:get_argument_value(42) * 100
   elseif module == "Ka-50" then
      rotor_rpm_percent = main_panel:get_argument_value(52) * 100
	  doors = string.format("%.2f", main_panel:get_argument_value(533))
   elseif module == "UH-1H" then
      rotor_rpm_percent = main_panel:get_argument_value(123) * 100
      doors = string.format(
        "%.2f, %.2f",
        main_panel:get_argument_value(420),
        main_panel:get_argument_value(422)
      )
   else
      -- Unsupported helicopter or not a helicopter.
      rotor_rpm_percent = 0
   end

   -- total count "rounds" of ammo, main cannon + all the pylons.
   local payload = LoGetPayloadInfo()
   if payload then
     ammo = payload.Cannon.shells
   	  local stations = LoGetPayloadInfo().Stations
   	  for i, st in pairs(stations) do
   			ammo = ammo .. string.format(", %d", st.count) -- for now only count, no types
   		end
   	end

   local payload = string.format(
      "---\n" ..
      "module: %s\n" ..
      "rotor_rpm_percent: %.16f\n" ..
	  "ammo: [%s]\n" ..
	  "doors: [%s]\n",
      module,
      rotor_rpm_percent,
      ammo,
      doors
   )

   socket.try(shksynsocket:send(payload))
end

function LuaExportStop()
   socket.try(shksynsocket:send("{}"))
   shksynsocket:close()
end

function LuaExportActivityNextEvent(t)
end
