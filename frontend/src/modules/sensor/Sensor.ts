import { InputType } from './inputType'

export interface Sensor {
  readonly key: InputType
  isAvailable: boolean
  isActive: boolean
  isCalibrated: boolean

  checkAvailability(): Promise<void>

  clone(): Sensor
}
