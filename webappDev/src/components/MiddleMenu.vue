<template>
    <span @click="()=>emit('statusClicked')" :class="'status ' + (sockApi.isConnected.value ? 'bg-green' : 'bg-red')">
        {{ sockApi.isConnected.value ? 'Connected' : 'Reconnecting' }}
    </span>
    <template v-if="props.state === null">
        <v-progress-circular style="margin: auto;" color="primary" indeterminate :size="58"
            :width="6"></v-progress-circular>
    </template>
    <template v-else>

        <v-btn v-if="!isFullscreen" @click="onRequestFullScreen" size="x-large">
            Open in fullscreen
        </v-btn>

        <v-spacer></v-spacer>

        <EmojiButton :state="props.state" @clicked="emoji=>sockApi.socket.emit('emoji', { type: emoji })" />

        <v-spacer></v-spacer>
        <v-btn size="x-large" prepend-icon="mdi-gas-station-outline" :color="props.state.pump ? 'green' : 'red'"
            variant="elevated" @click="onPumpToggled">
            Pump: {{ props.state.pump ? 'On' : 'Off' }}
        </v-btn>
        <v-btn size="x-large" prepend-icon="mdi-tank" :color="props.state.tank ? 'green' : 'red'" variant="elevated"
            @click="onTankToggled">
            Tank: {{ props.state.tank ? 'Open' : 'Closed' }}
        </v-btn>
    </template>
</template>

<script setup lang="ts">
import { useFullscreen } from '@/directives/UseFullscreen';
import { useSocketio } from '@/directives/UseSocketio';
import { type ServerState } from '@/Server';
import EmojiButton from './EmojiButton.vue';

const props = defineProps<{
    state: ServerState | null;
}>()

const emit = defineEmits<{
    (e: 'statusClicked'): void
}>()

// Websocket to communicate with
const sockApi = useSocketio();

// If the device is in fullscreen
const isFullscreen = useFullscreen();

// #region UI-Events

function onRequestFullScreen() {
    document.body.requestFullscreen();
}

// Event: When the pump button is pressed
function onPumpToggled() {
    sockApi.socket.emit('pump', { state: !props.state?.pump });
}

// Event: When the tank button is pressed
function onTankToggled() {
    sockApi.socket.emit('tank', { state: !props.state?.tank });
}

// #endregion

</script>

<style lang="scss">
.status {
    text-align: center;
    font-size: 150%;
    padding: 5px 10px;
    border-radius: 99999px;
}
</style>