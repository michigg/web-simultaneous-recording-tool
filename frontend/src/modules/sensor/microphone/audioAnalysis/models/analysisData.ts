import { AnalysisConfig } from './analysisConfig'

export class AnalysisData {
  readonly config: AnalysisConfig
  private startTimestamp: number = Date.now()
  private stopTimestamp: number = Date.now()
  readonly timestamps: Array<number> = []
  protected amplitudeSpectrums: Array<Float32Array> = []
  // Excluded for performance reasons
  // protected dbs: Array<number> = []
  protected dbas: Array<number> = []

  constructor(analysisConfig: AnalysisConfig = new AnalysisConfig()) {
    this.config = analysisConfig
  }

  public addData(spectrum: Float32Array, dba: number) {
    console.log('ADD DATA')
    if (spectrum.length === 0) {
      this.startTimestamp = Date.now()
    }
    this.stopTimestamp = Date.now()
    this.timestamps.push(this.stopTimestamp - this.startTimestamp)
    this.amplitudeSpectrums.push(spectrum)
    this.dbas.push(dba)
  }

  public clear() {
    this.startTimestamp = Date.now()
    this.stopTimestamp = Date.now()
    this.amplitudeSpectrums = []
  }

  public getAmplitudeSpectrums(): Array<Float32Array> {
    return this.amplitudeSpectrums
  }

  // Excluded for performance reasons
  // public getDBs (): Array<number> {
  //   return this.dbs
  // }

  public getDBAs(): Array<number> {
    return this.dbas
  }

  public getStartTimestamp(): number {
    return this.startTimestamp
  }

  public getStopTimestamp(): number {
    return this.stopTimestamp
  }

  toString() {
    const duration = (
      (this.stopTimestamp - this.startTimestamp) /
      1000
    ).toFixed(0)
    return `ProdAnalyzeData:\nDuration: ${duration}\tEntries: ${this.timestamps.length}`
  }
}
