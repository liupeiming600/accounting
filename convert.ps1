$files = @('06.csv','07.csv','08.csv','09.csv','10.csv')
foreach ($file in $files) {
    $path = "C:\Users\liu\accounting\2025\$file"
    $content = Get-Content $path -Encoding UTF8
    $utf8BOM = New-Object System.Text.UTF8Encoding $true
    [System.IO.File]::WriteAllLines($path, $content, $utf8BOM)
    Write-Host "$file 已转换为UTF-8 BOM"
}
Write-Host "全部完成!"
