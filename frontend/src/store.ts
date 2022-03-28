import { InjectionKey } from 'vue'
import { createStore, useStore as baseUseStore, Store } from 'vuex'
import { sensorStore } from './modules/sensor/store'

// define your typings for the store state
// eslint-disable-next-line @typescript-eslint/no-empty-interface
interface State {}

// define injection key
export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore({
  strict: import.meta.env.NODE_ENV !== 'production',
  modules: {
    sensor: sensorStore,
  },
})

export function useStore() {
  return baseUseStore(key)
}
