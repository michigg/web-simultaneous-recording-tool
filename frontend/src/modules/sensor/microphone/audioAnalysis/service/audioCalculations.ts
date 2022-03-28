const LOWEST_AUDIBLE_FREQUENCY = 20
const HIGHEST_AUDIBLE_FREQUENCY = 20000 // 70000
const AUDITORY_THRESHOLD = 0.00002 // Auditory Threshold 0.00002 Pa
// eslint-disable-next-line
const PAIN_THRESHOLD = 200 // Pain Threshold 200 Pa

export const AudioCalculations = {
  calcFrequencyResolution(sampleRate: number, bufferSize: number): number {
    return Number((sampleRate / bufferSize).toFixed(4))
  },
  calcFrequency(binIndex: number, frequencyResolution: number): number {
    return +(binIndex * frequencyResolution).toFixed(4)
  },
  calcFrequenciesUsingFrequencyResolution(
    frequencyResolution: number,
    bufferSize: number
  ): Array<number> {
    const frequencies = []
    for (let i = 0; i < bufferSize / 2; i++) {
      frequencies.push(this.calcFrequency(i, frequencyResolution))
    }
    return frequencies
  },
  calcFrequencies(sampleRate: number, bufferSize: number): Array<number> {
    const frequencyResolution = this.calcFrequencyResolution(
      sampleRate,
      bufferSize
    )
    return this.calcFrequenciesUsingFrequencyResolution(
      frequencyResolution,
      bufferSize
    )
  },
  calcLowestAudibleBin(
    frequencyResolution: number,
    lowestAudibleFrequency = LOWEST_AUDIBLE_FREQUENCY
  ): number {
    const calculatedLowestAudibleBin =
      lowestAudibleFrequency / frequencyResolution
    const lowestAudibleBin = Math.floor(calculatedLowestAudibleBin)
    if (lowestAudibleBin !== calculatedLowestAudibleBin) {
      return lowestAudibleBin + 1
    }
    return lowestAudibleBin
  },
  calcHighestAudibleBin(
    frequencyResolution: number,
    highestAudibleFrequency = HIGHEST_AUDIBLE_FREQUENCY
  ): number {
    return Math.trunc(highestAudibleFrequency / frequencyResolution)
  },
  calcAudibleBins(
    input: Array<number> | Float32Array,
    lowestAudibleBin: number,
    highestAudibleBin: number
  ): Array<number> | Float32Array {
    return input.slice(lowestAudibleBin, highestAudibleBin)
  },
  calcAWeighting(frequency: number): number {
    // Used formular shown at
    // https://www.schweizer-fn.de/akustik/schallpegelaenderung/schallpegel.php#berech_schallpegel_bewertungfaktoren
    const fSquared = Math.pow(frequency, 2)
    const aSquared = 148693636 // 148693636, 12194^2
    const bSquared = 423.9481 // 20.59^2
    const cSquared = 11577.76 // 107.6^2
    const dSquared = 544348.84 // 737.8^2

    // 12194^2 * f^4
    const numerator = aSquared * Math.pow(fSquared, 2)
    // (f^2 + 20.6^2) * sqrt((f^2 * 107.7^2) (f^2 * 737.9^2) (f^2 * 12194^2))

    const denominator =
      +(fSquared + aSquared).toFixed(8) *
      +(fSquared + bSquared).toFixed(8) *
      +Math.sqrt(fSquared + cSquared).toFixed(8) *
      +Math.sqrt(fSquared + dSquared).toFixed(8)
    // console.log((fSquared + aSquared), (fSquared + bSquared), Math.sqrt(fSquared + cSquared), Math.sqrt(fSquared + dSquared))
    // console.log(+(fSquared + aSquared).toFixed(8), +(fSquared + bSquared).toFixed(8), +Math.sqrt(fSquared + cSquared).toFixed(8), +Math.sqrt(fSquared + dSquared).toFixed(8))
    const a = +(numerator / denominator).toFixed(8)
    const aWeight = 20 * Math.log10(a) + 2
    return Number(aWeight.toFixed(1))
  },
  calcAWeightings(frequencies: Array<number>, minDB = -80.0): Array<number> {
    const weights = []
    for (const frequency of frequencies) {
      const weight = this.calcAWeighting(frequency)
      weights.push(weight > minDB ? weight : minDB)
    }
    return weights
  },
  calcDB(magnitude: number): number {
    if (magnitude < AUDITORY_THRESHOLD) {
      return 0
    }
    const db = 20.0 * Math.log10(magnitude / AUDITORY_THRESHOLD)
    return db
  },
  calcSpectrumDBs(spectrum: Float32Array | Array<number>): Array<number> {
    const dbs = []
    for (let i = 0; i < spectrum.length; i++) {
      dbs.push(this.calcDB(spectrum[i]))
    }
    return dbs
  },
  calcSpectrumRmsDB(spectrum: Float32Array): number {
    return this.calcRMS(this.calcSpectrumDBs(spectrum))
  },
  calcRMS(dbs: Array<number>): number {
    const sum = dbs.reduce((pv, cv) => pv + this.calcDBLogRevision(cv) ** 2, 0)
    return +(10 * Math.log10(+Math.sqrt(sum / dbs.length))).toFixed(2)
  },
  /**
   * @deprecated please use the performant <code>calcDBAWithWeighting</code>
   * @param magnitude
   * @param frequency
   */
  toDBAWithFrequency(magnitude: number, frequency: number): number {
    return this.calcDBAWithWeighting(magnitude, this.calcAWeighting(frequency))
  },
  calcDBAWithWeighting(magnitude: number, aWeighting: number): number {
    const db = this.calcDB(magnitude)
    const dba = db + aWeighting
    // return dba < 0 ? 0 : +(dba.toFixed(2))
    return +dba.toFixed(4)
  },
  calcSpectrumDBAs(
    spectrum: Float32Array,
    frequencies: Array<number>
  ): Array<number> {
    const dbas = []
    for (let i = 0; i < spectrum.length; i++) {
      dbas.push(this.toDBAWithFrequency(spectrum[i], frequencies[i]))
    }
    return dbas
  },
  calcDBAsFromSpectrumAndWeights(
    spectrum: Float32Array,
    aWeights: Array<number>
  ): Array<number> {
    const dbas = []
    for (let i = 0; i < spectrum.length; i++) {
      dbas.push(this.calcDBAWithWeighting(spectrum[i], aWeights[i]))
    }
    return dbas
  },
  calcDBA(dbas: Array<number>): number {
    return this.calcRMS(dbas)
  },
  calcMaxDBA(dbas: Array<number>): number {
    return Math.max(...dbas)
  },
  calcMinDBA(dbas: Array<number>): number {
    return Math.min(...dbas)
  },
  calcLeq(dbs: Array<number>) {
    let sum = 0
    for (const db of dbs) {
      sum += this.calcDBLogRevision(db)
    }
    return +(10 * Math.log10(sum)).toFixed(2)
  },
  // TODO: Test and better name
  calcNLeq(dbs: Array<number>) {
    let sum = 0
    for (const db of dbs) {
      sum += this.calcDBLogRevision(db)
    }
    return +(10 * Math.log10(sum / dbs.length)).toFixed(2)
  },
  calcDBLogRevision(db: number): number {
    return Math.pow(10, db / 10)
  },
}
