// eslint-disable-next-line
// @ts-ignore
import Meyda, { MeydaAnalyzer, MeydaFeaturesObject } from 'meyda'
import { AnalysisData } from '../models/analysisData'
import { MicSensor } from '../../Sensor'
import { AnalysisConfig } from '../models/analysisConfig'
import { AudioAnalysisService } from './audioAnalysisService'

export class MicAnalyzer {
  private analyzer: MeydaAnalyzer | undefined = undefined
  private readonly mic: MicSensor
  readonly analysisConfig: AnalysisConfig
  private readonly audioCalculationService: AudioAnalysisService
  private store: AnalysisData = new AnalysisData()

  constructor(mic: MicSensor) {
    this.mic = mic
    this.analysisConfig = new AnalysisConfig(
      undefined,
      mic.sampleRate,
      mic.bufferSize
    )
    this.audioCalculationService = new AudioAnalysisService(
      this.analysisConfig.sampleRate,
      this.analysisConfig.bufferSize,
      this.analysisConfig.lowestPerceptibleFrequency,
      this.analysisConfig.highestPerceptibleFrequency
    )
  }

  private async startAnalyzer(inputDevice: MediaDeviceInfo | undefined) {
    console.info('[AudioDBAnalyzer]: Try to start analyzer')
    if (typeof Meyda === 'undefined') {
      console.error(
        '[AudioDBAnalyzer]: Meyda could not be found! Have you included it?'
      )
      return
    }
    try {
      // INIT store
      this.store = new AnalysisData(this.analysisConfig)
      await this.mic.activateInputDevice(inputDevice?.deviceId)
      console.log('MIC', this.mic)

      // START Analyze
      this.analyzer = Meyda.createMeydaAnalyzer({
        audioContext: this.mic.audioContext,
        source: this.mic.sourceAudioNode,
        sampleRate: this.mic.sampleRate,
        bufferSize: this.mic.bufferSize,
        windowingFunction: this.analysisConfig.windowingFunction,
        featureExtractors: ['amplitudeSpectrum'],
        callback: (features: MeydaFeaturesObject) => {
          // Excluded for performance reasons
          // const db = this.audioCalculationService.getDB(features.amplitudeSpectrum)
          // const dba = this.audioCalculationService.calcSpectrumDBA(features.amplitudeSpectrum)
          // this.store.addData(features.amplitudeSpectrum, db, dba)
          this.store.addData(features.amplitudeSpectrum, 0)
        },
      })
      this.analyzer.start()
      console.info('[AudioDBAnalyzer]: Analyzer started')
    } catch (e) {
      console.error('[AudioDBAnalyzer]: Analyzer start failed', e)
    }
  }

  private async stopAnalyzer() {
    console.info('[AudioDBAnalyzer]: Try to stop analyzer')
    if (!this.analyzer) {
      console.warn('[AudioDBAnalyzer]: No analyzer to stop found')
      return
    }
    try {
      this.analyzer.stop()
      await this.mic.deactivateInputDevices()
      console.info('[AudioDBAnalyzer]: ANALYZER STOP')
    } catch (e) {
      console.error('[AudioDBAnalyzer]: Analyzer stop failed', e)
    }
  }

  async analyze(
    durationSecondsOverride = 0,
    inputDevice: MediaDeviceInfo | undefined = undefined
  ): Promise<AnalysisData> {
    await this.startAnalyzer(inputDevice)
    const duration =
      durationSecondsOverride || this.analysisConfig.durationSeconds
    this.analysisConfig.durationSeconds = duration
    const onAnalyzeStop = new Promise<void>((resolve) => {
      setTimeout(async () => {
        await this.stopAnalyzer()
        resolve()
      }, duration * 1000)
    })
    await onAnalyzeStop
    return this.store
  }
}
