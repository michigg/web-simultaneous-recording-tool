import { DTO } from './DTO'

interface Base {
  version: string
  testId: string
  description: string
  testIteration: number
}

export class BaseDTO implements DTO<Base> {
  readonly version: string = '1'
  readonly jsonKey: string = 'base'
  readonly testId: string
  readonly description: string
  readonly testIteration: number // previously testNumber

  constructor(testId: string, description: string, testIteration: number) {
    this.testId = testId
    this.description = description
    this.testIteration = testIteration
  }

  static fromJSON(json: {
    testId?: string
    description?: string
    testIteration?: number
  }): BaseDTO | undefined {
    if (!json || !json.testId || !json.description) {
      return undefined
    }

    if (!json.testIteration || json.testIteration < 0) {
      return undefined
    }

    return new BaseDTO(json.testId, json.description, json.testIteration)
  }

  toJSON() {
    return {
      version: this.version,
      testId: this.testId,
      description: this.description,
      testIteration: this.testIteration,
    }
  }
}
