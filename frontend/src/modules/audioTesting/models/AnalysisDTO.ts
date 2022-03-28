import { DTO } from './DTO'

export class AnalysisDTO {
  private readonly version = '1'
  readonly dtos: Array<DTO<unknown>>

  constructor(dtos: Array<DTO<unknown>> = []) {
    this.dtos = dtos
  }

  toJSON(): unknown {
    const json: { [index: string]: unknown } = {}
    for (const dto of this.dtos) {
      json[dto.jsonKey] = dto.toJSON()
    }
    json.version = this.version
    return json
  }
}
