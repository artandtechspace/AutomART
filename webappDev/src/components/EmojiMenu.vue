<template>
    <!-- Menu Content with Blur Background -->
    <div class="emoji-menu-background pa-4">
        <v-row dense>
            <v-col v-for="(emoji, index) in EMOJIS" :key="index" cols="4" class="d-flex justify-center">
                <v-btn size="x-large" class="emoji-btn" elevation="2" color="white" style="font-size: 24px;"
                    @click="emit('clicked', index.toString())">
                    {{ emoji }}
                </v-btn>
            </v-col>
        </v-row>
        <v-btn color="red" class="d-block mt-10" style="margin: auto" size="x-large" @click="emit('closed')">
            Close
        </v-btn>
    </div>
</template>

<script lang="ts" setup>
import { EMOJIS } from '@/Config';

const emit = defineEmits<{
    (e: 'clicked', emoji: string): void
    (e: 'closed'): void
}>()


</script>

<style lang="scss">
// Emoji-Menu
.emoji-menu-background {
    border-radius: 8px;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>