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
        content = RuleProcessor.filter_DOMAIN_REGEX(content)
        return content

        # 过滤DOMAIN-REGEX类型的规则，因为客户端目前不支持
		@staticmethod
		def filter_DOMAIN_REGEX(content: str) -> str:
			lines = content.splitlines()
			processed_lines = [
				line for line in lines 
				if not 'DOMAIN-REGEX' in line
			]
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