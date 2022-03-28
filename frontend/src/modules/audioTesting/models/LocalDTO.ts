import { DTO } from './DTO'

interface Local {
  version: string
  deviceName: string
  inputDeviceInfo: MediaDeviceInfo
}

export class LocalDTO implements DTO<Local> {
  readonly version: string = '1'
  readonly jsonKey: string = 'local'
  readonly deviceName: string
  readonly inputDeviceInfo: MediaDeviceInfo

  constructor(deviceName: string, inputDeviceInfo: MediaDeviceInfo) {
    this.deviceName = deviceName
    this.inputDeviceInfo = inputDeviceInfo
  }

  toJSON() {
    return {
      version: this.version,
      deviceName: this.deviceName,
      inputDeviceInfo: this.inputDeviceInfo,
    }
  }
}
