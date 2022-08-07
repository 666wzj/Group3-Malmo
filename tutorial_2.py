from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

from builtins import range
import MalmoPython
import os
import sys
import time
import json

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# More interesting generator string: "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"


# Create default Malmo objects:

#mission_file = './tutorial_2.xml'
#with open(mission_file, 'r') as f:
    #print("Loading mission from %s" % mission_file)
    #mission_xml = f.read()
mission_xml ='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <About>
    <Summary>Cliff walking mission based on Sutton and Barto.</Summary>
  </About>

  <ServerSection>
    <ServerInitialConditions>
        <Time><StartTime>1</StartTime></Time>
    </ServerInitialConditions>
    <ServerHandlers>
      <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
      <DrawingDecorator>
        <!-- coordinates for cuboid are inclusive -->
        <DrawCuboid x1="-3" y1="46" z1="-3" x2="8" y2="50" z2="14" type="air" />            <!-- limits of our arena -->
        <DrawCuboid x1="7" y1="45" z1="-2" x2="-2" y2="45" z2="13" type="lava" />          
        <DrawCuboid x1="6"  y1="45" z1="-1"  x2="-1" y2="45" z2="12" type="sandstone" />      <!-- floor of the arena -->
        <DrawBlock x="-1"  y="45" z="12" type="lapis_block" />     <!-- the destination marker -->
      </DrawingDecorator>
      <ServerQuitFromTimeUp timeLimitMs="50000"/>
      <ServerQuitWhenAnyAgentFinishes/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>Cristina</Name>
    <AgentStart>
      <Placement x="6.5" y="46.0" z="-0.5" pitch="30" yaw="0"/>
    </AgentStart>
    <AgentHandlers>
      <ContinuousMovementCommands/>
      <ObservationFromFullStats/>
      <RewardForTouchingBlockType>
        <Block reward="-100.0" type="lava" behaviour="onceOnly"/>
        <Block reward="100.0" type="lapis_block" behaviour="onceOnly"/>
        
      </RewardForTouchingBlockType>
      <RewardForSendingCommand reward="-1" />
      <AgentQuitFromTouchingBlockType>
          <Block type="lava" />
          <Block type="lapis_block" />
      </AgentQuitFromTouchingBlockType>
    </AgentHandlers>
  </AgentSection>

</Mission>
'''

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

my_mission = MalmoPython.MissionSpec(mission_xml, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')

#start

while True:
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    if world_state.is_mission_running and len(world_state.observations) > 0 :
        #for observation in world_state.observations:
            #print(observation)
        #XPos=float(world_state.observations[0].text.split(',')[-7].split(':')[-1])
        obs_text = world_state.observations[-1].text
        obs = json.loads(obs_text)
        p_ZPos=obs['ZPos']

        break
print(p_ZPos)
time.sleep(1)

cishu=3
for _ in range(0,cishu):

    agent_host.sendCommand("move 0.5")
    while True:
        time.sleep(0.05)
        world_state = agent_host.getWorldState()
        if world_state.is_mission_running and len(world_state.observations) > 0:
            # for observation in world_state.observations:
            # print(observation)
            # XPos=float(world_state.observations[0].text.split(',')[-7].split(':')[-1])
            obs_text = world_state.observations[-1].text
            obs = json.loads(obs_text)

            if (abs(abs(float(p_ZPos) - float(obs['ZPos'])) - 1) < 0.1):
                agent_host.sendCommand("move 0")
                p_ZPos += 1
                break

    print(p_ZPos)
    print(obs['ZPos'])














# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission ended")
# Mission has ended.
