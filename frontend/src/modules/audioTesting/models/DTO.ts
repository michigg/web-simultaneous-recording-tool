export interface DTO<T> {
  readonly version: string
  readonly jsonKey: string

  toJSON(): T
}
