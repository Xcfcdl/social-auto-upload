import { createPinia } from 'pinia'
import { useUserStore } from './user'
import { useAccountStore } from './account'
import { useAppStore } from './app'
import { useSora2Store } from './sora2'

const pinia = createPinia()

export default pinia
export { useUserStore, useAccountStore, useAppStore, useSora2Store }