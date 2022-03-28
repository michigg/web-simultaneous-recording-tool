import { DTO } from './DTO'
import { AnalysisData } from '../../sensor/microphone/audioAnalysis/models/analysisData'
import { AudioAnalysisService } from '../../sensor/microphone/audioAnalysis/service/audioAnalysisService'

interface Audio {
  version: string
  durationSeconds: number
  sampleRate: number
  bufferSize: number
  numberOfInputChannels: number
  windowingFunction: string
  lowestPerceptibleFrequency: number
  highestPerceptibleFrequency: number
  frequencies: number[]
  startTimestamp: number
  stopTimestamp: number
  timestamps: number[]
  amplitudeSpectrums: string[]
  dbas: number[]
  maxDBA: number
  minDBA: number
  dbaRMS: number
}

export class AudioDTO implements DTO<Audio> {
  readonly version: string = '1'
  readonly jsonKey: string = 'audio'
  readonly durationSeconds: number
  readonly bufferSize: number
  readonly sampleRate: number
  readonly numberOfInputChannels: number
  readonly windowingFunction: string
  readonly frequencies: Array<number>
  readonly lowestPerceptibleFrequency: number
  readonly highestPerceptibleFrequency: number

  readonly startTimestamp: number
  readonly stopTimestamp: number
  readonly timestamps: Array<number>

  readonly amplitudeSpectrums: Array<Float32Array>
  // readonly dbs: Array<number>
  readonly dbas: Array<number>
  readonly dbaRMS: number
  readonly dbaLEQ: number
  readonly maxDBA: number
  readonly minDBA: number

  constructor(
    durationSeconds: number,
    sampleRate: number,
    bufferSize: number,
    numberOfInputChannels: number,
    windowingFunction: string,
    lowestPerceptibleFrequency: number,
    highestPerceptibleFrequency: number,
    frequencies: Array<number>,
    startTimestamp: number,
    stopTimestamp: number,
    timestamps: Array<number>,
    amplitudeSpectrums: Array<Float32Array>,
    // dbs: Array<number>,
    dbas: Array<number>,
    dbaRMS: number,
    dbaLEQ: number,
    maxDBA: number,
    minDBA: number
  ) {
    this.durationSeconds = durationSeconds
    this.sampleRate = sampleRate
    this.bufferSize = bufferSize
    this.numberOfInputChannels = numberOfInputChannels
    this.windowingFunction = windowingFunction
    this.lowestPerceptibleFrequency = lowestPerceptibleFrequency
    this.highestPerceptibleFrequency = highestPerceptibleFrequency
    this.frequencies = frequencies

    this.startTimestamp = startTimestamp
    this.stopTimestamp = stopTimestamp
    this.timestamps = timestamps

    this.amplitudeSpectrums = amplitudeSpectrums
    // this.dbs = dbs
    this.dbas = dbas
    this.dbaRMS = dbaRMS
    this.dbaLEQ = dbaLEQ
    this.maxDBA = maxDBA
    this.minDBA = minDBA
  }

  static fromAnalysisData(analysisData: AnalysisData): AudioDTO {
    const audioAnalysisService = new AudioAnalysisService(
      analysisData.config.sampleRate,
      analysisData.config.bufferSize,
      analysisData.config.lowestPerceptibleFrequency,
      analysisData.config.highestPerceptibleFrequency
    )
    const { dbas, maxDBA, minDBA, dbaRMS, dbaLEQ } =
      audioAnalysisService.getAnalysisData(analysisData.getAmplitudeSpectrums())
    return new AudioDTO(
      analysisData.config.durationSeconds,
      analysisData.config.sampleRate,
      analysisData.config.bufferSize,
      analysisData.config.numberOfInputChannels,
      analysisData.config.windowingFunction,
      analysisData.config.lowestPerceptibleFrequency,
      analysisData.config.highestPerceptibleFrequency,
      analysisData.config.frequencies,
      analysisData.getStartTimestamp(),
      analysisData.getStopTimestamp(),
      analysisData.timestamps,
      analysisData.getAmplitudeSpectrums(),
      // analysisData.getDBs(),
      dbas,
      dbaRMS,
      dbaLEQ,
      maxDBA,
      minDBA
    )
  }

  toJSON() {
    const jsonAmplitudeSpectrums = this.amplitudeSpectrums.map((arr) =>
      JSON.stringify(Array.from(arr))
    )
    return {
      version: this.version,
      durationSeconds: this.durationSeconds,
      sampleRate: this.sampleRate,
      bufferSize: this.bufferSize,
      numberOfInputChannels: this.numberOfInputChannels,
      windowingFunction: this.windowingFunction,
      lowestPerceptibleFrequency: this.lowestPerceptibleFrequency,
      highestPerceptibleFrequency: this.highestPerceptibleFrequency,
      frequencies: this.frequencies,
      startTimestamp: this.startTimestamp,
      stopTimestamp: this.stopTimestamp,
      timestamps: this.timestamps,
      amplitudeSpectrums: jsonAmplitudeSpectrums,
      dbas: this.dbas,
      maxDBA: this.maxDBA,
      minDBA: this.minDBA,
      dbaRMS: this.dbaRMS,
    }
  }
}
