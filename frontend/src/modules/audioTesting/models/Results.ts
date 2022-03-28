export class Results {
  analysisTitle: string
  fileNames: Array<string>
  filePaths: Array<string>

  constructor(
    analysisTitle: string,
    fileNames: Array<string>,
    filePaths: Array<string>
  ) {
    this.analysisTitle = analysisTitle
    this.fileNames = fileNames
    this.filePaths = filePaths
  }
}
