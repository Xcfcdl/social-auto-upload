# 清理脚本 - 用于git filter-branch
if (Test-Path 'myUtils/sora2_generator.py') {
    # 读取文件内容
    $content = Get-Content 'myUtils/sora2_generator.py'
    
    # 替换API密钥
    $updatedContent = $content -replace 'API_KEY = "sk-5vdtIM5RNun4CT9LDmBHkXvjowmpYKslhPqfURRbn7RL62fy"', 'API_KEY = os.environ.get("SORA2_API_KEY")'
    
    # 写回文件
    $updatedContent | Set-Content 'myUtils/sora2_generator.py'
    
    Write-Host "已更新 myUtils/sora2_generator.py 文件中的API密钥配置"
}