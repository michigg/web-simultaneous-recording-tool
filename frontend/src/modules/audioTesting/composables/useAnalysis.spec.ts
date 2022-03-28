import { useAnalysis } from './useAnalysis'

describe('useAnalysis', () => {
  let analysis: ReturnType<typeof useAnalysis>
  let socket: {
    emit: jest.Mock
    on: jest.Mock
  }

  beforeEach(() => {
    socket = {
      emit: jest.fn(),
      on: jest.fn(),
    }
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    analysis = useAnalysis(socket)
  })
  describe('submit', () => {
    it('emits start_analysis for ground truth', () => {
      analysis.submit({
        testId: 'GROUND_TRUTH',
        description: 'A short description about the test problem.',
        testIteration: 1,
        frogPosition: '',
        frogSize: '',
        frogId: -1,
        penBrand: '',
        penId: -1,
        clickCount: -1,
        distanceKey: '50cm',
        durationInSeconds: 5,
        noisePreset: '40_DBA',
        noiseType: 'WHITE_NOISE',
      })
      const expected = {
        version: '1',
        base: {
          version: '1',
          testId: 'GROUND_TRUTH',
          description: 'A short description about the test problem.',
          testIteration: 1,
        },
        distance: {
          version: '1',
          distanceKey: '50cm',
          distanceKeys: [
            '50cm',
            '0m',
            'CREDIT_H',
            'CREDIT_V',
            'A4_H',
            'A4_V',
            'SMALL_PERSON_SHOULDER_MAX',
            'MEDIUM_PERSON_SHOULDER_MAX',
            'SMALL_PERSON_ARM_MAX',
            'MEDIUM_PERSON_ARM_MAX',
          ],
        },
        duration: {
          version: '1',
          durationInSeconds: 5,
        },
        noisePreset: {
          version: '1',
          noisePreset: '40_DBA',
          noisePresets: [
            'BN',
            '40_DBA',
            '50_DBA',
            '60_DBA',
            '70_DBA',
            '80_DBA',
            '90_DBA',
          ],
          noiseType: 'WHITE_NOISE',
          noiseTypes: ['WHITE_NOISE', 'PINK_NOISE'],
        },
      }
      expect(socket.emit).toHaveBeenCalledTimes(1)
      expect(socket.emit).toHaveBeenNthCalledWith(1, 'start_analysis', expected)
    })

    it('emits start_analysis for frog test', () => {
      analysis.submit({
        testId: 'FROG',
        description: 'A short description about the test problem.',
        testIteration: 1,
        frogPosition: 'OPEN_FINGER',
        frogSize: 'LARGE',
        frogId: 1,
        penBrand: '',
        penId: -1,
        clickCount: 5,
        distanceKey: '0m',
        durationInSeconds: 5,
        noisePreset: '',
        noiseType: '',
      })
      const expected = {
        version: '1',
        base: {
          version: '1',
          testId: 'FROG',
          description: 'A short description about the test problem.',
          testIteration: 1,
        },
        distance: {
          version: '1',
          distanceKey: '0m',
          distanceKeys: [
            '50cm',
            '0m',
            'CREDIT_H',
            'CREDIT_V',
            'A4_H',
            'A4_V',
            'SMALL_PERSON_SHOULDER_MAX',
            'MEDIUM_PERSON_SHOULDER_MAX',
            'SMALL_PERSON_ARM_MAX',
            'MEDIUM_PERSON_ARM_MAX',
          ],
        },
        clickCount: {
          version: '1',
          clickCount: 5,
        },
        frog: {
          version: '1',
          frogId: 1,
          frogPosition: 'OPEN_FINGER',
          frogPositions: [
            'OPEN_FINGER',
            'OPEN_THUMB',
            'CLOSED_FINGER',
            'CLOSED_THUMB',
          ],
          frogSize: 'LARGE',
          frogSizes: ['SMALL', 'LARGE'],
        },
        duration: {
          version: '1',
          durationInSeconds: 5,
        },
      }
      expect(socket.emit).toHaveBeenCalledTimes(1)
      expect(socket.emit).toHaveBeenNthCalledWith(1, 'start_analysis', expected)
    })

    it('emits start_analysis for pen test', () => {
      analysis.submit({
        testId: 'PEN',
        description: 'A short description about the test problem.',
        testIteration: 1,
        frogPosition: '',
        frogSize: '',
        frogId: -1,
        penBrand: 'UNKNOWN',
        penId: 1,
        clickCount: 5,
        distanceKey: '0m',
        durationInSeconds: 5,
        noisePreset: '',
        noiseType: '',
      })
      const expected = {
        version: '1',
        base: {
          version: '1',
          testId: 'PEN',
          description: 'A short description about the test problem.',
          testIteration: 1,
        },
        distance: {
          version: '1',
          distanceKey: '0m',
          distanceKeys: [
            '50cm',
            '0m',
            'CREDIT_H',
            'CREDIT_V',
            'A4_H',
            'A4_V',
            'SMALL_PERSON_SHOULDER_MAX',
            'MEDIUM_PERSON_SHOULDER_MAX',
            'SMALL_PERSON_ARM_MAX',
            'MEDIUM_PERSON_ARM_MAX',
          ],
        },
        clickCount: {
          version: '1',
          clickCount: 5,
        },
        pen: {
          version: '1',
          penId: 1,
          penBrand: 'UNKNOWN',
          penBrands: ['UNKOWN_COLORED', 'DATEV_GREEN'],
        },
        duration: {
          version: '1',
          durationInSeconds: 5,
        },
      }
      expect(socket.emit).toHaveBeenCalledTimes(1)
      expect(socket.emit).toHaveBeenNthCalledWith(1, 'start_analysis', expected)
    })
  })
})
