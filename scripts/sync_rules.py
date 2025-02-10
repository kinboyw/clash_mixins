import os
import yaml
import requests
from typing import List, Callable

class RuleProcessor:
    @staticmethod
    def process_rule(content: str) -> str:
        """
        处理规则的基础函数，可以在这里添加自定义的处理逻辑
        """
        content = RuleProcessor.filter_unsupported_rules(content)
        return content

    # 过滤不支持的规则
    @staticmethod
    def filter_unsupported_rules(content: str) -> str:
        """
        过滤不支持的规则类型,包括DOMAIN-REGEX和IP-ASN
        
        Args:
            content: 包含规则的字符串内容
            
        Returns:
            过滤后的规则内容字符串
        """
        # 定义不支持的规则类型
        unsupported_rules = ['DOMAIN-REGEX', 'IP-ASN']
        
        # 按行分割内容
        lines = content.splitlines()
        
        # 过滤掉包含不支持规则的行
        processed_lines = []
        for line in lines:
            # 检查是否包含不支持的规则类型
            if not any(rule in line for rule in unsupported_rules):
                processed_lines.append(line)
                
        # 重新组合成字符串
        return '\n'.join(processed_lines)

def ensure_directory(filepath: str) -> None:
    """确保输出目录存在"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

def sync_rules():
    # 读取配置文件
    with open('config/rules.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    processor = RuleProcessor()
    
    # 处理每个规则
    for rule in config['rules']:
        url = rule['url']
        output_path = rule['output']
        
        try:
            # 下载规则文件
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            
            # 处理规则
            processed_content = processor.process_rule(content)
            
            # 保存处理后的规则
            ensure_directory(output_path)
            with open(output_path, 'w') as f:
                f.write(processed_content)
                
            print(f"Successfully processed {url} -> {output_path}")
            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

if __name__ == '__main__':
    sync_rules()