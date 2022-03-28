import { DTO } from './DTO'

interface Click {
  version: string
  clickCount: number
}

export class ClickDTO implements DTO<Click> {
  readonly version: string = '1'
  readonly jsonKey: string = 'clickCount'
  readonly clickCount: number

  constructor(clickCount: number) {
    this.clickCount = clickCount
  }

  static fromJSON(json: { clickCount?: number }): ClickDTO | undefined {
    if (!json || !json.clickCount || json.clickCount === -1) {
      return undefined
    }
    return new ClickDTO(json.clickCount)
  }

  toJSON() {
    return {
      version: this.version,
      clickCount: this.clickCount,
    }
  }
}
