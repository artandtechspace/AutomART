<template>
    <v-menu close-on-content-click v-model="emojiMenuOpen" transition="scale-transition">
        <template v-slot:activator="{ props }">
            <v-btn color="primary" class="position-absolute" style="bottom: 1.5rem; right: 1.5rem" icon="mdi-plus"
                v-bind="props"></v-btn>
        </template>

        <!-- Menu Content with Blur Background -->
        <div class="emoji-menu-background pa-4">
            <v-row dense>
                <v-col v-for="(emoji, index) in EMOJIS" :key="index" cols="4" class="d-flex justify-center">
                    <v-btn class="emoji-btn" elevation="2" color="white" style="font-size: 24px;"
                        @click="emit('clicked', index.toString())">
                        {{ emoji }}
                    </v-btn>
                </v-col>
            </v-row>
        </div>
    </v-menu>
</template>

<script lang="ts" setup>
import { EMOJIS } from '@/Conifg';

const emit = defineEmits<{
    (e: 'clicked', emoji: string): void
}>()


// If the menu is open
const emojiMenuOpen = ref(false);

</script>

<style lang="scss">
// Emoji-Menu
.emoji-menu-background {
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>