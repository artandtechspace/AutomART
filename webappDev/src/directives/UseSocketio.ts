import { onMounted } from 'vue'
import { io, Socket } from "socket.io-client";
import { type Ref, ref } from "vue"
import { ADDRESS } from '../Config'




type SocketAPI = {
    isConnected: Ref<Boolean>,
    socket: Socket;
};

// Singleton that stores the socket api and socket
let socketSingelton: SocketAPI | undefined;


export function useSocketio() : SocketAPI {
    if(socketSingelton !== undefined)
        return socketSingelton;

    console.log("[Socket] Init socket");

    // Gets the address
    let addr = ADDRESS;
    if(addr === 'AUTO')
        addr = location.host;

    const socket = io(`http://${addr}/`, {
        transports: ['websocket'],
    });

    const refConnected: Ref<boolean> = ref(false);

    socket.on('connect', ()=>refConnected.value = true);
    socket.on('disconnect', ()=>refConnected.value = false);

    return {
        isConnected: refConnected,
        socket
    };
}