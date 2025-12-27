<template>
    <v-overlay v-model="emojiOverlayOpen" class="align-center justify-center">
        <EmojiMenu @clicked="onClickedEmoji" @closed="() => emojiOverlayOpen = false" />
    </v-overlay>

    <!-- Button to open the menu -->
    <v-btn v-if="displayEmoji === null" color="primary" style="margin: auto;" size="x-large" icon="mdi-plus"
        @click="emojiOverlayOpen = !emojiOverlayOpen"></v-btn>

    <!-- Playing emoji overlay -->
    <div v-else class="emoji-display">
        {{ displayEmoji }}
    </div>
</template>


<script setup lang="ts">
import { EMOJIS } from '@/Config';
import type { ServerState } from '@/Server';
import EmojiMenu from './EmojiMenu.vue';

const props = defineProps<{
    state: ServerState | null;
}>()

const emit = defineEmits<{
    (e: 'clicked', emoji: string): void
}>()

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


function onClickedEmoji(name: string) {
    emojiOverlayOpen.value = false;
    emit("clicked", name);
}

</script>

<style lang="scss">
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