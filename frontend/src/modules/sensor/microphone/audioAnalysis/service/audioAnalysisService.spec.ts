import { AudioAnalysisService } from './audioAnalysisService'

describe('AudioAnalysisService', () => {
  describe('calcSpectrumDBs', () => {
    it('should correctly initialize repositories', () => {
      const audioAnalysisService = new AudioAnalysisService(
        44100,
        2048,
        0,
        20000
      )
      const spectrum = Float32Array.from([0.00002, 0.00002, 200, 200])
      const dbSpectrum = [0, 0, 140, 140]
      expect(audioAnalysisService.calcSpectrumDBs(spectrum)).toStrictEqual(
        dbSpectrum
      )
    })
  })
  describe('calcSpectrumDBAs', () => {
    it('should correctly initialize repositories', () => {
      const audioAnalysisService = new AudioAnalysisService(
        44100,
        2048,
        0,
        20000
      )
      const spectrum = Float32Array.from([0.00002, 0.00002, 200, 200])
      // const frequencies = [21.5332, 43.0664, 64.5996, 86.1328]
      // const weights = [-80.0, -48.4984, -33.0876, -25.8045, -21.2874]
      // const dbs = [0, 0, 140, 140]
      // const dbas = [-80.0, -48.4984, 106.9124, 114.1955]
      const dbas = [-80.0, -48.5, 106.9, 114.2]
      expect(audioAnalysisService.calcSpectrumDBAs(spectrum)).toStrictEqual(
        dbas
      )
    })
  })
  describe('calcSpectrumDBA', () => {
    it('should return 114.94 when [0.00002, 0.00002, 200, 200] are given', () => {
      const audioAnalysisService = new AudioAnalysisService(
        44100,
        2048,
        0,
        20000
      )
      const spectrum = Float32Array.from([0.00002, 0.00002, 200, 200])
      // const frequencies = [21.5332, 43.0664, 64.5996, 86.1328]
      // const weights = [-80.0, -48.4984, -33.0876, -25.8045, -21.2874]
      // const dbs = [0, 0, 140, 140]
      // const dbas = [-80.0, -48.4984, 106.9124, 114.1955]
      // const ilog = [0.00000001, 0.000014131, 49117923684.3266, 262754401623.9962]
      // expect(audioAnalysisService.calcSpectrumDBA(spectrum)).toStrictEqual(114.94)
      expect(audioAnalysisService.calcSpectrumDBA(spectrum)).toStrictEqual(
        111.26
      )
    })
  })
})
