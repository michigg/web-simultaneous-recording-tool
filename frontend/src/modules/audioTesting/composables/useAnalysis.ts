import { ref } from 'vue'
import { Ref } from '@vue/reactivity'
import { MicSensor } from '../../sensor/microphone/Sensor'
import { MicAnalyzer } from '../../sensor/microphone/audioAnalysis/service/MicAnalyzer'
import { AnalysisDTO } from '../models/AnalysisDTO'
import { AudioDTO } from '../models/AudioDTO'
import { Socket } from 'socket.io-client'
import { DTO } from '../models/DTO'
import { BaseDTO } from '../models/BaseDTO'
import { DistanceDTO } from '../models/DistanceDTO'
import { FrogDTO } from '../models/FrogDTO'
import { Results } from '../models/Results'
import { DurationDTO } from '../models/DurationDTO'
import { WhiteNoisePresetsDTO } from '../models/WhiteNoisePresetsDTO'
import { LocalDTO } from '../models/LocalDTO'
import { PenDTO } from '../models/PenDTO'
import { ClickDTO } from '../models/ClickDTO'

export interface TestForm {
  testId: string
  description: string
  testIteration: number
  frogPosition: string
  frogSize: string
  frogId: number
  penBrand: string
  penId: number
  clickCount: number
  distanceKey: string
  durationInSeconds: number
  noisePreset: string
  noiseType: string
}

export function useAnalysis(socket: Socket): {
  isMaster: Ref<boolean>
  shallMasterRecorded: Ref<boolean>
  isAnalysing: Ref<boolean>
  results: Ref<Results>
  startLocalAnalyse: (
    durationInSeconds: number,
    dtos: Array<DTO<unknown>>
  ) => Promise<AnalysisDTO>
  startRemoteAnalyse: (config: Array<DTO<unknown> | undefined>) => void
  submit: (form: TestForm) => void
  micSensor: Ref<MicSensor>
  deviceName: Ref<string>
  inputDeviceInfo: Ref<{ label: string; value: MediaDeviceInfo } | undefined>
} {
  const isMaster = ref<boolean>(false)
  const shallMasterRecorded = ref<boolean>(false)
  const isAnalysing = ref<boolean>(false)
  const micSensor = ref<MicSensor>(new MicSensor())
  const micAnalyzer = new MicAnalyzer(micSensor.value)

  const deviceName = ref<string>('')
  const inputDeviceInfo = ref<
    { label: string; value: MediaDeviceInfo } | undefined
  >(undefined)

  const results = ref<Results>(new Results('', [], []))

  const startLocalAnalyse = async (
    durationInSeconds: number,
    dtos: Array<DTO<unknown>>
  ): Promise<AnalysisDTO> => {
    isAnalysing.value = true
    if (!inputDeviceInfo.value) {
      console.error(
        '[SOCKET]: [startLocalAnalyse]: Missing input device. Abort!'
      )
      throw Error('[SOCKET]: [startLocalAnalyse]: Missing input device. Abort!')
    }
    const localData = new LocalDTO(
      deviceName.value,
      inputDeviceInfo.value.value
    )
    const analysisData = await micAnalyzer.analyze(
      durationInSeconds,
      inputDeviceInfo.value.value
    )
    isAnalysing.value = false
    const audioDTO = AudioDTO.fromAnalysisData(analysisData)
    const mainDTO = new AnalysisDTO([audioDTO, localData, ...dtos])
    console.log('AUDIO DTO', mainDTO)
    return mainDTO
  }

  socket.on('start_measurement', async (data: { [key: string]: never }) => {
    const durationDTO = DurationDTO.fromJSON(data[DurationDTO.KEY])
    if (!durationDTO) {
      console.error(
        `[SOCKET]: [start_measurement]: Cannot start analysis. Duration is missing. ${data}`
      )
      return
    }
    const newDTOs = [
      BaseDTO.fromJSON(data.base),
      DistanceDTO.fromJSON(data.distance),
      FrogDTO.fromJSON(data.frog),
      WhiteNoisePresetsDTO.fromJSON(data.noisePreset),
      ClickDTO.fromJSON(data.clickCount),
      PenDTO.fromJSON(data.pen),
    ]
    const dtos = newDTOs.filter((dto) => !!dto) as DTO<unknown>[]
    console.info(
      `[SOCKET]: [start_measurement]: Record requested: ${dtos.toString()}`
    )
    if (isMaster.value && !shallMasterRecorded.value) {
      console.info(
        '[SOCKET]: [start_measurement]: Master will not be recorded.'
      )
      return
    }
    const analysisDTO = await startLocalAnalyse(
      durationDTO.durationInSeconds,
      dtos
    )
    console.info(
      '[SOCKET]: [start_measurement]: Try send record! ',
      analysisDTO.toJSON()
    )
    socket.emit('finished_analysis', analysisDTO.toJSON())
  })

  socket.on(
    'update_directory',
    async ({
      analysisTitle,
      fileNames: newFileNames,
      filePaths: newFilePaths,
    }: {
      analysisTitle: string
      fileNames: Array<string>
      filePaths: Array<string>
    }) => {
      console.debug(
        '[SOCKET]: [update_directory]: ',
        analysisTitle,
        newFileNames,
        newFilePaths
      )
      results.value = new Results(analysisTitle, newFileNames, newFilePaths)
    }
  )

  const startRemoteAnalyse = (config: Array<DTO<unknown> | undefined>) => {
    const filteredConfig = config.filter((value) => !!value) as Array<
      DTO<unknown>
    >
    const data = new AnalysisDTO(filteredConfig).toJSON()
    console.info('[SOCKET]: [startRecord]: Send Start Broadcast: ', data)
    socket.emit('start_analysis', data)
  }

  const submit = (form: TestForm) => {
    const newDTOs = [
      BaseDTO.fromJSON(form),
      DistanceDTO.fromJSON(form),
      FrogDTO.fromJSON(form),
      DurationDTO.fromJSON(form),
      WhiteNoisePresetsDTO.fromJSON(form),
      ClickDTO.fromJSON(form),
      PenDTO.fromJSON(form),
    ]
    const dtos = newDTOs.filter((dto) => !!dto)
    startRemoteAnalyse(dtos)
  }

  return {
    isMaster,
    shallMasterRecorded,
    isAnalysing,
    results,
    startLocalAnalyse,
    startRemoteAnalyse,
    submit,
    micSensor,
    deviceName,
    inputDeviceInfo,
  }
}
