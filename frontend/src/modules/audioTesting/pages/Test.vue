<script lang="ts" setup>
  import LayoutSingleColumn from '@/modules/base/components/LayoutSingleColumn.vue'
  import { useSocketConnection } from '@/modules/socket/composables/useSocketConnection'
  import CustomSection from '@/modules/base/components/CustomSection.vue'
  import InputGroup from '@/modules/base/components/input/InputGroup.vue'
  import State from '@/modules/audioTesting/components/State.vue'
  import FormBase from '@/modules/base/components/input/FormBase.vue'
  import SelectGroup from '@/modules/base/components/input/SelectGroup.vue'
  import InputGroupCheckbox from '@/modules/base/components/input/InputGroupCheckbox.vue'
  import ButtonBase from '@/modules/base/components/ButtonBase.vue'
  import InfoMeasurement from '@/modules/audioTesting/components/InfoMeasurement.vue'
  import { computed, ref } from 'vue'
  import { useAnalysis } from '@/modules/audioTesting/composables/useAnalysis'
  import { FrogDTO } from '@/modules/audioTesting/models/FrogDTO'
  import { DistanceDTO } from '@/modules/audioTesting/models/DistanceDTO'
  import { WhiteNoisePresetsDTO } from '@/modules/audioTesting/models/WhiteNoisePresetsDTO'
  import { useAudioSelect } from '@/modules/audioTesting/composables/useAudioSelect'
  import { PenDTO } from '@/modules/audioTesting/models/PenDTO'

  const { socket, userCount, isConnected } = useSocketConnection()

  const {
    isMaster,
    shallMasterRecorded,
    isAnalysing,
    results,
    submit,
    micSensor,
    deviceName,
    inputDeviceInfo,
  } = useAnalysis(socket)

  const form = ref({
    testId: '',
    description: '',
    testIteration: 1,
    frogPosition: '',
    frogSize: '',
    frogId: -1,
    penBrand: '',
    penId: -1,
    clickCount: -1,
    distanceKey: '',
    durationInSeconds: 8,
    noisePreset: '',
    noiseType: '',
  })
  const run = () => {
    submit(form.value)
  }
  const frogSizes = FrogDTO.frogSizes
  const frogPositions = FrogDTO.frogPositions
  const penBrands = PenDTO.penBrands
  const distances = DistanceDTO.distanceKeys
  const noiseTypes = WhiteNoisePresetsDTO.noiseTypes
  const noisePresets = WhiteNoisePresetsDTO.noisePresets

  const isReady = computed((): boolean => {
    return !!deviceName.value && !isAnalysing.value && isConnected.value
  })

  const { availableDevices } = useAudioSelect(micSensor)
  const deviceOptions = computed(() => {
    return availableDevices.value.map((device) => ({
      title: device.label,
      value: device,
    }))
  })
</script>

<template>
  <LayoutSingleColumn title="Simultaneous Audio Record Tool">
    <CustomSection>
      <h2>Local Settings</h2>
      <FormBase @submit.prevent="run">
        <InputGroup
          id="input-device-name"
          v-model.trim.uppercase="deviceName"
          label="DeviceName"
        />
        <p v-if="!inputDeviceInfo">No Input Device Selected!</p>
        <p v-else>
          {{ inputDeviceInfo.label }}
        </p>
        <SelectGroup
          id="input-audio-device"
          v-model="inputDeviceInfo"
          :options="deviceOptions"
          label="Microphones"
        />
      </FormBase>
    </CustomSection>

    <CustomSection>
      <h2>Info Panel</h2>
      <State
        :input-device="undefined"
        :is-recording="isAnalysing"
        :user-count="userCount"
        :is-ready="isReady"
      />
    </CustomSection>

    <CustomSection>
      <h2>Master Settings</h2>
      <h3>Recording Options</h3>
      <InputGroupCheckbox
        id="input-master-is"
        v-model="isMaster"
        label="Is Device Master?"
      />
      <InputGroupCheckbox
        id="input-shall-master-recorded"
        v-model="shallMasterRecorded"
        label="Shall Master Be Recorded?"
      />
      <FormBase v-if="isMaster" @submit.prevent="run">
        <h3>Test Options</h3>
        <InputGroup
          id="input-analysis-name"
          v-model.uppercase.trim="form.testId"
          label="Test ID"
          required
        />
        <label for="input-analysis-description">Test Description</label>
        <textarea
          id="input-analysis-description"
          v-model.trim="form.description"
          required
        />
        <InputGroup
          id="input-test-number"
          v-model="form.testIteration"
          label="Test Number"
          type="number"
          min="1"
          max="5"
          required
        />

        <h3>Frog Options</h3>
        <SelectGroup
          id="input-frog-size"
          v-model="form.frogSize"
          :options="frogSizes"
          label="Frog Size"
        />
        <InputGroup
          id="input-frog-id"
          v-model="form.frogId"
          label="Frog ID"
          type="number"
          min="-1"
          max="3"
        />
        <SelectGroup
          id="input-frog-position"
          v-model="form.frogPosition"
          :options="frogPositions"
          label="Frog Position"
        />

        <h3>Pen Options</h3>
        <SelectGroup
          id="input-pen-brand"
          v-model="form.penBrand"
          :options="penBrands"
          label="Pen Brand"
        />
        <InputGroup
          id="input-pen-id"
          v-model="form.penId"
          label="Pen ID"
          type="number"
          min="-1"
          max="3"
        />

        <h3>Distance Options</h3>
        <SelectGroup
          id="input-distance"
          v-model="form.distanceKey"
          :options="distances"
          label="Distance"
        />

        <h3>Noise Options</h3>
        <SelectGroup
          id="input-noise-type"
          v-model="form.noiseType"
          :options="noiseTypes"
          label="Noise Type"
        />

        <SelectGroup
          id="input-noise-presets"
          v-model="form.noisePreset"
          :options="noisePresets"
          label="Noise Presets"
        />

        <h3>Click Count Options</h3>
        <InputGroup
          id="input-click-count"
          v-model="form.clickCount"
          label="Click Count"
          type="number"
          min="-1"
          max="20"
          step="1"
        />

        <h3>Analysis Duration</h3>
        <InputGroup
          id="input-duration"
          v-model="form.durationInSeconds"
          label="Duration (in seconds)"
          type="number"
          min="1"
          max="60"
          step="1"
          required
        />
        <template #actions>
          <ButtonBase type="submit">
            Analyse on all connected devices
          </ButtonBase>
        </template>
      </FormBase>
    </CustomSection>

    <CustomSection v-if="isMaster">
      <h2>Last Measurement Info</h2>
      <h3>Last Measurement Config</h3>
      TODO: Implement
      <h3>Last Measurement Results</h3>
      <InfoMeasurement :results="results" />
    </CustomSection>
  </LayoutSingleColumn>
</template>
<style scoped></style>
