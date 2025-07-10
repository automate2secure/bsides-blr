-- bttp-version-enum.nse
-- First iteration by ChatGPT.
-- Description:
--   Enumerates version, users, and files for a custom TCP protocol on port 13375.
--   The protocol uses a message format that starts with "#bsides# " and ends with " #end".
--
-- Categories: safe, discovery
--
-- Usage:
--   nmap -p 13375 --script bttp-version-enum <target>
--
-- Author: ChatGPT, Rahul

local nmap = require "nmap"
local shortport = require "shortport"
local stdnse = require "stdnse"

-- Define the port and protocol details
portrule = shortport.port_or_service(13375, "unknown", "tcp")

-- Function to communicate with the custom protocol
local function send_command(host, port, command)
  local proto_prefix = "#bsides# "
  local proto_suffix = " #end#"
  local request = proto_prefix .. command .. proto_suffix
  local response = ""

  local conn = nmap.new_socket()
  conn:set_timeout(5000)
  
  local status, err = conn:connect(host, port)
  if not status then
    return nil, ("Connection failed: %s"):format(err)
  end

  -- process the welcome message
  local status, msg = conn:receive()
  if msg:match("^#bsides# Welcome to the BSides") then
    stdnse.print_debug(1, "DEBUG: Received Welcome Message: %s", tostring(msg))
  end

  -- Send the command
  conn:send(request .. "\n")
  
  -- Receive the response
  while true do
    local status, line = conn:receive_lines(1)
    stdnse.print_debug("server response: %s", tostring(line))
    stdnse.print_debug("server status: %s", tostring(status))
    if line then
      response = response .. line:gsub("[\r\n]", "")
      break
    end
  end

  conn:close()

  -- Check if the response is in the expected format
  stdnse.print_debug(1, "Checking Response %s", tostring(response))
  if response:match("^#bsides#") and response:match("#end#$") then
    stdnse.print_debug(1, "Response matches our expectations..")
    response = response:gsub("#bsides# ", "")
    response = response:gsub(" #end#", "")
    return response
  else
    return "Invalid response format"
  end
end

-- Main action function
action = function(host, port)
  local output = {}

  -- Enumerate version
  local version_response = send_command(host, port, "version")
  if version_response then
    table.insert(output, "Protocol Version: " .. version_response)
  else
    table.insert(output, "Failed to get version.")
  end

  -- Enumerate users
  local users_response = send_command(host, port, "list_users")
  if users_response then
    table.insert(output, "Users: " .. users_response)
  else
    table.insert(output, "Failed to get users.")
  end

  -- Enumerate files
  local files_response = send_command(host, port, "list_files")
  if files_response then
    table.insert(output, "Files: " .. files_response)
  else
    table.insert(output, "Failed to get files.")
  end

  return stdnse.format_output(true, output)
end
