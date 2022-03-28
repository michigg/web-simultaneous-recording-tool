import { onMounted, ref, watch } from 'vue'
import { MicSensor } from '../../sensor/microphone/Sensor'
import { Ref } from '@vue/reactivity'

export function useAudioSelect(mic: Ref<MicSensor>): {
  availableDevices: Ref<Array<MediaDeviceInfo>>
  audioDevice: Ref<MediaDeviceInfo | undefined>
} {
  const availableDevices = ref<Array<MediaDeviceInfo>>([])
  const audioDevice = ref<MediaDeviceInfo | undefined>(undefined)

  onMounted(async () => {
    console.log('MIC', mic)
    await mic.value.getPermission()
    availableDevices.value = await mic.value.availableDevices()
    if (availableDevices.value.length > 0) {
      audioDevice.value = availableDevices.value[0]
    }
    console.log('MOUNTED FINISHED', audioDevice.value)
  })
  console.log(mic)
  watch(mic, async (currentMic) => {
    await currentMic.getPermission()
    availableDevices.value = await currentMic.availableDevices()
    if (availableDevices.value.length > 0) {
      audioDevice.value = availableDevices.value[0]
    }
    console.log('MOUNTED FINISHED', audioDevice.value)
  })
  return {
    availableDevices,
    audioDevice,
  }
}
