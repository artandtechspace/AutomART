<template>

    <div class="overlay-speed">
        <h1>Speed modifier</h1>

        <v-slider class="mt-8" v-model="model" thumb-label="always"></v-slider>
    </div>

</template>

<script setup lang="ts">

const model = defineModel<number>();

</script>

<style lang="scss">
.overlay-speed {
    background: rgba(210, 210, 210, 0.58);
    border-radius: 10px;
    padding: 1rem;
    min-width: 80vw;
}
</style>