<#
启动本地预览：先把 docs 中的 .rst 转为 HTML，然后在 docs/_preview_html 启动静态 HTTP 服务

示例：
  # 在 PowerShell 中执行（默认端口 8000）
  .\scripts\serve_preview.ps1

参数：
  -Port <int>  HTTP 服务端口，默认 8000

依赖：Python 3、docutils
  pip install docutils
#>
param(
	[int]$Port = 8000
)

try {
	Write-Host "1) 生成 HTML 预览到 docs/_preview_html/"
	python .\scripts\preview_rst.py | Write-Host
} catch {
	Write-Error "转换失败。请确认已安装 Python 和 docutils（pip install docutils）。"
	exit 1
}

$previewDir = Join-Path -Path "docs" -ChildPath "_preview_html"
if (-not (Test-Path $previewDir)) {
	Write-Error "预览目录不存在: $previewDir"
	exit 2
}

Write-Host "2) 在 http://localhost:$Port 提供静态服务（目录: $previewDir）"
Push-Location $previewDir
try {
	Start-Process "http://localhost:$Port"
	python -m http.server $Port
} finally {
	Pop-Location
}
