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

    <v-main>
      <!-- Control Joystick -->
      <Joystick class="joystick" @change="onJoyStick" />

      <template v-if="sockApi.isConnected.value">
        <!-- Playing emoji overlay -->
        <div v-if="currentEmoji != null" class="position-absolute emoji-display">
          {{ currentEmoji }}
        </div>
        <!-- Menu to select emojis -->
        <EmojiMenu v-else @clicked="onEmojiClicked" />
      </template>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { useSocketio } from './directives/UseSocketio';
import { EMOJIS } from './Conifg';

// Current emoji
const currentEmoji: Ref<string | null> = ref(null);

// Socketio api
const sockApi = useSocketio();
sockApi.socket.on('e_status', onStatusRetreived);


// Event: When a status update from the server is retreived
function onStatusRetreived({ emoji }: { emoji: string | null }) {
  // Updates emoji in ui
  if (emoji == null || EMOJIS[emoji] === undefined)
    currentEmoji.value = null;
  else
    currentEmoji.value = EMOJIS[emoji];
}

// Sends the joystick inputs to the server
function onJoyStick(angle: number, distance: number) {
  if (distance > 200) distance = 200;

  angle += Math.PI / 2
  if (angle > Math.PI)
    angle -= 2 * Math.PI

  // Sends the data
  sockApi.socket.emit("joystick", { angle, dist: distance / 200 });
}

// Event: When an emoji is clicked
function onEmojiClicked(name: string) {
  sockApi.socket.emit("emoji", { type: name });
}

</script>

<style lang="scss">
.joystick {
  display: block;
  width: 90%;
  height: 90%;
  margin: 5%;
  background: rgb(215, 215, 215);
  border: 1vw dashed gray;
  border-radius: 1rem;
}

.status {
  padding: 5px 10px;
  border-radius: 99999px;
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