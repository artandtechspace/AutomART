<template>
    <div ref="refElm"></div>
</template>


<script lang="ts" setup>
import JoystickController from "joystick-controller";
import { ref } from "vue";

//const props = defineProps<{}>()

const emit = defineEmits<{
    (e: 'change', angle: number, speed: number): void
}>()

let joystick: JoystickController | undefined = undefined;

const refElm = ref(null);

onMounted(()=>{

    joystick = new JoystickController({
        maxRange: 200,
        level: 100,
        radius: 40,
        joystickRadius: 25,
        opacity: 0.8,
        distortion: false,
        dynamicPosition: true,
        dynamicPositionTarget: refElm.value,
        mouseClickButton: "ALL",
        hideContextMenu: true,
    }, (data) => emit('change', data.angle, data.distance));
})

onUnmounted(()=> {

    if(joystick === undefined)
        return;

    joystick.destroy();
})
</script>