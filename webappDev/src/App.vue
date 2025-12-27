<template>
  <v-app>
    <v-main class="main">

      <div class="grid-main">
        <div class="grid-item grid-left">
          <Joystick @change="n=>onJoyStick(true,n)" class="joystick" />
        </div>
        <div class="grid-item grid-center">
          <MiddleMenu :state="serverStatus" />
        </div>
        <div class="grid-item grid-right">
          <Joystick @change="n=>onJoyStick(false,n)" class="joystick" />
        </div>
      </div>

    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { useSocketio } from './directives/UseSocketio';
import Joystick from './components/Joystick.vue';
import MiddleMenu from './components/MiddleMenu.vue';
import { type ServerState } from "./Server"

// Current status
const serverStatus: Ref<ServerState | null> = ref(null)

const joyStickPositions: Ref<{
  r: number,
  l: number
}> = ref({
  r: 0,
  l: 0
})

// Socketio api
const sockApi = useSocketio();
sockApi.socket.on('e_status', status => serverStatus.value = status);



function onJoyStick(isRight: boolean, y: number) {
    if(isRight)
      joyStickPositions.value.r = y;
    else
      joyStickPositions.value.l = y;

  // Sends the data
  sockApi.socket.emit("joystick_tank", {
    l: joyStickPositions.value.l, r: joyStickPositions.value.r
  });
}

</script>

<style lang="scss">
:root {
  --general-padding: 10px;
}

.main {
  background-image: url("/rsc/Background.png");
  background-size: 100% 100%;
}

.grid-main {
  display: flex;
  height: 100%;
}

.grid-left,
.grid-right {
  flex-grow: 1;
}

.grid-center {
  padding: var(--general-padding);
  display: flex;
  flex-direction: column;
  gap: var(--general-padding);
  min-width: 30vw;
}

.joystick {
  display: block;
  width: 90%;
  height: 90%;
  margin: 5%;
  background: rgba(215, 215, 215, 0.527);
  border: 4px dotted gray;
  border-radius: 1rem;
}
</style>