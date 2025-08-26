/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { createPinia } from 'pinia'
import VuetifyPlugin from "./plugins/VuetifyPlugin"

// Styles
import 'unfonts.css'

const app = createApp(App)

// Registers plugins
app.use(createPinia());
app.use(VuetifyPlugin);

app.mount('#app')
