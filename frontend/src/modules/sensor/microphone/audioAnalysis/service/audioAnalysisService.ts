import { AudioCalculations } from './audioCalculations'

const LOWEST_AUDIBLE_FREQUENCY = 20 // lowest frequency a human can hear
const HIGHEST_AUDIBLE_FREQUENCY = 20000 // highest frequency a human can hear

export class AudioAnalysisService {
  readonly lowestAudibleBin: number
  readonly highestAudibleBin: number
  readonly aWeights: Array<number>

  constructor(
    sampleRate: number,
    bufferSize: number,
    lowestaudiblefrequency = LOWEST_AUDIBLE_FREQUENCY,
    highestAudibleFrequency = HIGHEST_AUDIBLE_FREQUENCY
  ) {
    const frequencyResolution = AudioCalculations.calcFrequencyResolution(
      sampleRate,
      bufferSize
    )
    this.lowestAudibleBin = AudioCalculations.calcLowestAudibleBin(
      frequencyResolution,
      lowestaudiblefrequency
    )
    this.highestAudibleBin = AudioCalculations.calcHighestAudibleBin(
      frequencyResolution,
      highestAudibleFrequency
    )

    const frequencies = AudioCalculations.calcFrequencies(
      sampleRate,
      bufferSize
    )
    const weightings = AudioCalculations.calcAWeightings(frequencies)
    this.aWeights = <Array<number>>(
      AudioCalculations.calcAudibleBins(
        weightings,
        this.lowestAudibleBin,
        this.highestAudibleBin
      )
    )
    console.log('BINS', this.lowestAudibleBin, this.highestAudibleBin)
  }

  calcSpectrumDBAs(spectrum: Float32Array): Array<number> {
    const audibleSpectrum = <Float32Array>(
      AudioCalculations.calcAudibleBins(
        spectrum,
        this.lowestAudibleBin,
        this.highestAudibleBin
      )
    )
    const dbas = []
    for (let i = 0; i < audibleSpectrum.length; i++) {
      dbas.push(
        AudioCalculations.calcDBAWithWeighting(
          audibleSpectrum[i],
          this.aWeights[i]
        )
      )
    }
    return dbas
  }

  calcSpectrumsDBAs(spectrums: Array<Float32Array>): Array<number> {
    const dbas = []
    for (const spectrum of spectrums) {
      dbas.push(this.calcSpectrumDBA(spectrum))
    }
    return dbas
  }

  getAnalysisData(spectrums: Array<Float32Array>): {
    dbas: Array<number>
    maxDBA: number
    minDBA: number
    dbaRMS: number
    dbaLEQ: number
  } {
    const dbas = this.calcSpectrumsDBAs(spectrums)
    const maxDBA = AudioCalculations.calcMaxDBA(dbas)
    const minDBA = AudioCalculations.calcMinDBA(dbas)
    const dbaRMS = AudioCalculations.calcRMS(dbas)
    const dbaLEQ = AudioCalculations.calcNLeq(dbas)
    return {
      dbas,
      maxDBA,
      minDBA,
      dbaRMS,
      dbaLEQ,
    }
  }

  calcSpectrumDBA(spectrum: Float32Array): number {
    const dbas = this.calcSpectrumDBAs(spectrum)
    return AudioCalculations.calcRMS(dbas)
  }

  calcSpectrumDBs(spectrum: Float32Array): Array<number> {
    const audibleSpectrum = <Float32Array>(
      AudioCalculations.calcAudibleBins(
        spectrum,
        this.lowestAudibleBin,
        this.highestAudibleBin
      )
    )
    return AudioCalculations.calcSpectrumDBs(audibleSpectrum)
  }

  calcSpectrumDB(spectrum: Float32Array): number {
    const audibleSpectrum = <Float32Array>(
      AudioCalculations.calcAudibleBins(
        spectrum,
        this.lowestAudibleBin,
        this.highestAudibleBin
      )
    )
    return AudioCalculations.calcSpectrumRmsDB(audibleSpectrum)
  }
}
