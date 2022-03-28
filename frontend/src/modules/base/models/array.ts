export function reduceArrayToSize(
  arr: Array<Float32Array | string | number>,
  maxSize: number
) {
  if (arr.length > maxSize) {
    arr.shift()
  }
}
