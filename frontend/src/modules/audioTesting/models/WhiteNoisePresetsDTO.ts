import { DTO } from './DTO'

interface WhiteNoisePresets {
  version: string
  noiseType: string
  noiseTypes: string[]
  noisePreset: string
  noisePresets: string[]
}

export class WhiteNoisePresetsDTO implements DTO<WhiteNoisePresets> {
  readonly version: string = '1'
  readonly jsonKey: string = 'noisePreset'
  readonly noiseType: string
  static readonly noiseTypes: Array<string> = ['WHITE_NOISE', 'PINK_NOISE']

  readonly noisePreset: string
  static readonly noisePresets: Array<string> = [
    'BN',
    '40_DBA',
    '50_DBA',
    '60_DBA',
    '70_DBA',
    '80_DBA',
    '90_DBA',
  ]

  constructor(noiseType: string, noisePreset: string) {
    this.noiseType = noiseType
    this.noisePreset = noisePreset
  }

  static fromJSON(json: {
    noiseType?: string
    noisePreset?: string
  }): WhiteNoisePresetsDTO | undefined {
    if (!json || !json.noiseType || !json.noisePreset) {
      return undefined
    }
    return new WhiteNoisePresetsDTO(json.noiseType, json.noisePreset)
  }

  toJSON() {
    return {
      version: this.version,
      noiseType: this.noiseType,
      noiseTypes: WhiteNoisePresetsDTO.noiseTypes,
      noisePreset: this.noisePreset,
      noisePresets: WhiteNoisePresetsDTO.noisePresets,
    }
  }
}
