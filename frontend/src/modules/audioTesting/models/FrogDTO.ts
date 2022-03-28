import { DTO } from './DTO'

interface Frog {
  version: string
  frogId: number
  frogSize: string
  frogSizes: string[]
  frogPosition: string
  frogPositions: string[]
}

export class FrogDTO implements DTO<Frog> {
  readonly version: string = '1'
  readonly jsonKey: string = 'frog'
  readonly frogId: number
  readonly frogSize: string
  static readonly frogSizes: Array<string> = ['SMALL', 'LARGE']

  readonly frogPosition: string
  static readonly frogPositions: Array<string> = [
    'OPEN_FINGER',
    'OPEN_THUMB',
    'CLOSED_FINGER',
    'CLOSED_THUMB',
  ]

  constructor(frogId: number, frogSize: string, frogPosition: string) {
    this.frogId = frogId
    this.frogSize = frogSize
    this.frogPosition = frogPosition
  }

  static fromJSON(json: {
    frogId?: number
    frogSize?: string
    frogPosition?: string
  }): FrogDTO | undefined {
    if (!json || !json.frogId || !json.frogSize || !json.frogPosition) {
      return undefined
    }
    return new FrogDTO(json.frogId, json.frogSize, json.frogPosition)
  }

  toJSON() {
    return {
      version: this.version,
      frogId: this.frogId,
      frogSize: this.frogSize,
      frogSizes: FrogDTO.frogSizes,
      frogPosition: this.frogPosition,
      frogPositions: FrogDTO.frogPositions,
    }
  }
}
