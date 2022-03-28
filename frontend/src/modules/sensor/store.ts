import { Commit } from 'vuex'
import { Sensor } from './Sensor'
import { InputType } from './inputType'
import { MicSensor } from './microphone/Sensor'

interface SensorState {
  sensors: Map<InputType, Sensor>
}

export const SET_SENSOR = 'SET_SENSOR'

export const sensorStore = {
  namespaced: true,
  state(): SensorState {
    return {
      sensors: new Map<InputType, Sensor>([[InputType.MIC, new MicSensor()]]),
    }
  },
  getters: {
    getSensor: (state: SensorState) => (sensorKey: InputType) => {
      const sensor = state.sensors.get(sensorKey)
      if (!sensor) {
        return undefined
      }
      return sensor.clone()
    },
  },
  mutations: {
    [SET_SENSOR](state: SensorState, sensor: Sensor) {
      state.sensors.set(sensor.key, sensor)
    },
  },
  actions: {
    async checkAvailability({
      state,
      commit,
    }: {
      state: SensorState
      commit: Commit
    }) {
      for (const sensor of state.sensors.values()) {
        const cloneSensor = sensor.clone()
        await cloneSensor.checkAvailability()
        commit(SET_SENSOR, cloneSensor)
      }
    },
    async updateSensor({ commit }: { commit: Commit }, sensor: Sensor) {
      commit(SET_SENSOR, sensor)
    },
  },
}
