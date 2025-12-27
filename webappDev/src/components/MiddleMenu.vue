<template>
    <span :class="'status ' + (sockApi.isConnected.value ? 'bg-green' : 'bg-red')">
        {{ sockApi.isConnected.value ? 'Connected' : 'Reconnecting' }}
    </span>
    <template v-if="props.state === null">
        <v-progress-circular style="margin: auto;" color="primary" indeterminate :size="58"
            :width="6"></v-progress-circular>
    </template>
    <template v-else>
        <v-overlay v-model="emojiOverlayOpen" class="align-center justify-center">
            <EmojiMenu @clicked="onEmojiClicked" @closed="() => emojiOverlayOpen = false" />
        </v-overlay>

        <v-btn v-if="!isFullscreen" @click="onRequestFullScreen" size="x-large">
            Open in fullscreen
        </v-btn>

        <v-spacer></v-spacer>

        <v-btn v-if="displayEmoji === null" color="primary" style="margin: auto;" size="x-large" icon="mdi-plus"
            @click="emojiOverlayOpen = !emojiOverlayOpen"></v-btn>
        <!-- Playing emoji overlay -->
        <div v-else class="emoji-display">
            {{ displayEmoji }}
        </div>

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
import EmojiMenu from './EmojiMenu.vue';
import { EMOJIS } from '@/Config';

const props = defineProps<{
    state: ServerState | null;
}>()

// Websocket to communicate with
const sockApi = useSocketio();

// If the device is in fullscreen
const isFullscreen = useFullscreen();

// If the emoji-overlay is open
const emojiOverlayOpen = ref(false);



// Actual emoji that is shown
const displayEmoji = computed(() => {
    if (
        props.state === null || props.state.emoji === null ||
        EMOJIS[props.state.emoji] === undefined
    )
        return null;

    return EMOJIS[props.state.emoji];
})

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

// Event: When an emoji is clicked
function onEmojiClicked(name: string) {
    sockApi.socket.emit("emoji", { type: name });
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

.emoji-display {
    user-select: none;

    background-color: rgba(255, 255, 255, 0.6);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    border-radius: 8px;
    padding: 1rem;
    font-size: 400%;

    width: min-content;
    margin: auto;

    animation: softBounce 1.5s ease-out infinite;
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