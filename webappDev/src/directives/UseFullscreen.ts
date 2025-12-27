import { onMounted } from 'vue'
import { type Ref, type ComputedRef, ref } from "vue"


export function useFullscreen() : Ref<boolean> {
    
    const fullscreen: Ref<boolean> = ref(false);

    function onFire(){
        fullscreen.value = document.fullscreenElement !== null;
    }

    onMounted(()=>document.addEventListener('fullscreenchange', onFire));
    onUnmounted(()=>document.removeEventListener('fullscreenchange', onFire));

    return fullscreen;
}