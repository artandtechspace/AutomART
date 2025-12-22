<template>
  <v-app>
    <v-app-bar color="primary">
      <v-app-bar-title>Rieke's AutomART</v-app-bar-title>

      <template v-slot:append>
        <span :class="'status ' + (sockApi.isConnected.value ? 'bg-green' : 'bg-red')">
          {{ sockApi.isConnected.value ? 'Connected' : 'Reconnecting' }}
        </span>
      </template>
    </v-app-bar>

    <v-main class="main">
      <!-- Control Joystick -->
      <Joystick class="joystick" @change="onJoyStick" />

      <!-- Emoji overlay -->
      <template v-if="sockApi.isConnected.value">
        <!-- Playing emoji overlay -->
        <div v-if="displayEmoji != null" class="position-absolute emoji-display">
          {{ displayEmoji }}
        </div>
        <!-- Menu to select emojis -->
        <EmojiMenu v-else @clicked="onEmojiClicked" />
      </template>

      <!-- Pump and Tank overlay -->
      <v-card
        color="gray"
        density="compact"
        v-if="serverStatus !== null" 
        class="position-absolute pump-display" title="Pump & Tank System" variant="outlined">
        <v-card-actions>
          <v-btn
            prepend-icon="mdi-gas-station-outline"
            :color="serverStatus.pump ? 'green' : 'red'"
            variant="elevated"
            @click="onPumpToggled"
            >
            Pump: {{ serverStatus.pump ? 'On' : 'Off' }}
          </v-btn>
          <v-btn
          prepend-icon="mdi-tank"
          :color="serverStatus.tank ? 'green' : 'red'"
          variant="elevated"
          @click="onTankToggled">
            Tank: {{ serverStatus.tank ? 'Open' : 'Closed' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { useSocketio } from './directives/UseSocketio';
import { EMOJIS } from './Config';
import { RefSymbol } from '@vue/reactivity';
import EmojiMenu from './components/EmojiMenu.vue';
import Joystick from './components/Joystick.vue';
import { server } from 'typescript';

// Current status
const serverStatus: Ref<{
  emoji: string,
  tank: boolean,
  pump: boolean
} | null> = ref(null)


// Actual emoji that is shown
const displayEmoji = computed(()=>{
  if(
    serverStatus.value === null || serverStatus.value.emoji === null ||
    EMOJIS[serverStatus.value.emoji] === undefined
  )
    return null;

  return EMOJIS[serverStatus.value.emoji];
})

// Socketio api
const sockApi = useSocketio();
sockApi.socket.on('e_status', status => serverStatus.value = status);

// Sends the joystick inputs to the server
function onJoyStick(angle: number, distance: number) {
  if (distance > 200) distance = 200;

  angle += Math.PI / 2
  if (angle > Math.PI)
    angle -= 2 * Math.PI

  // Sends the data
  sockApi.socket.emit("joystick", { angle, dist: distance / 200 });
}

// Event: When the pump button is pressed
function onPumpToggled(){
  sockApi.socket.emit('pump', { state: !serverStatus.value?.pump });
}

// Event: When the tank button is pressed
function onTankToggled(){
  sockApi.socket.emit('tank', { state: !serverStatus.value?.tank });
}

// Event: When an emoji is clicked
function onEmojiClicked(name: string) {
  sockApi.socket.emit("emoji", { type: name });
}

</script>

<style lang="scss">

.main {
  background-image: url("/rsc/Background.png");
  background-size: 100% 100%;
}

.joystick {
  display: block;
  width: 90%;
  height: 90%;
  margin: 5%;
  background: rgba(215, 215, 215, 0.527);
  border: 1vw dashed gray;
  border-radius: 1rem;
}

.status {
  padding: 5px 10px;
  border-radius: 99999px;
}

.pump-display {
  user-select: none;
  bottom: 1.5rem;
  left: 1.5rem;
  background: white !important
}

// Shows currently playing emoji
.emoji-display {
  user-select: none;
  bottom: 1.5rem;
  right: 1.5rem;

  background-color: rgba(255, 255, 255, 0.6);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 8px;
  padding: 1rem;
  font-size: 400%;

  animation: softBounce 1.5s ease-out infinite;
}

.settings-menu-background {

  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

@keyframes softBounce {
  0% {
    transform: translateY(0);
  }

  10% {
    transform: translateY(-10px);
  }

  40% {
    transform: translateY(-0px);
  }

  100% {
    transform: translateY(0);
  }
}
</style>