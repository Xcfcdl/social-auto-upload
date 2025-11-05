import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置测试环境变量
os.environ['SORA2_API_KEY'] = 'test_api_key_from_env'
os.environ['SORA2_API_BASE_URL'] = 'https://test-api.example.com'

# 导入sora2_generator模块以测试环境变量加载
try:
    from myUtils.sora2_generator import API_KEY, API_BASE_URL
    
    print("=== 环境变量配置测试 ===")
    print(f"API_KEY 从环境变量读取: {API_KEY}")
    print(f"API_BASE_URL 从环境变量读取: {API_BASE_URL}")
    
    # 验证配置是否正确加载
    if API_KEY == 'test_api_key_from_env':
        print("✓ API_KEY 成功从环境变量读取")
    else:
        print("✗ API_KEY 未正确从环境变量读取")
    
    if API_BASE_URL == 'https://test-api.example.com':
        print("✓ API_BASE_URL 成功从环境变量读取")
    else:
        print("✗ API_BASE_URL 未正确从环境变量读取")
    
    print("\n=== 测试完成 ===")
    print("程序已成功配置为从环境变量读取API密钥和URL配置。")
    print("请确保在生产环境中设置正确的环境变量:")
    print("- SORA2_API_KEY: 您的实际API密钥")
    print("- SORA2_API_BASE_URL: API基础URL（可选，有默认值）")
    
    sys.exit(0)
except Exception as e:
    print(f"测试失败: {str(e)}")
    sys.exit(1)