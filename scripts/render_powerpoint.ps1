param(
    [Parameter(Mandatory = $true)][string]$InputPptx,
    [Parameter(Mandatory = $true)][string]$OutputPng,
    [int]$Width = 3600
)
$ErrorActionPreference = 'Stop'
$taskSource = (Resolve-Path -LiteralPath $InputPptx).Path
$taskDestination = [System.IO.Path]::GetFullPath($OutputPng)
[System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($taskDestination)) | Out-Null
$taskPowerPoint = $null
$taskDeck = $null
$taskPreviousCount = -1
try {
    $taskPowerPoint = New-Object -ComObject PowerPoint.Application
    $taskPreviousCount = $taskPowerPoint.Presentations.Count
    $taskDeck = $taskPowerPoint.Presentations.Open($taskSource, -1, 0, 0)
    $taskHeight = [int][math]::Round($Width * $taskDeck.PageSetup.SlideHeight / $taskDeck.PageSetup.SlideWidth)
    $taskDeck.Slides.Item(1).Export($taskDestination, 'PNG', $Width, $taskHeight)
    Write-Output ('Rendered with PowerPoint: ' + $taskDestination + '; shapes=' + $taskDeck.Slides.Item(1).Shapes.Count)
} finally {
    if ($taskDeck) {
        $taskDeck.Close()
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskDeck)
    }
    if ($taskPowerPoint) {
        if ($taskPreviousCount -eq 0 -and $taskPowerPoint.Presentations.Count -eq 0) { $taskPowerPoint.Quit() }
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskPowerPoint)
    }
}
