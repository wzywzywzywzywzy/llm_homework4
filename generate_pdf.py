import markdown
import pdfkit
import os

def generate_pdf():
    # 读取README.md文件
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # 读取SUBMISSION_GUIDE.md文件
    with open('SUBMISSION_GUIDE.md', 'r', encoding='utf-8') as f:
        guide_content = f.read()
    
    # 将Markdown转换为HTML
    readme_html = markdown.markdown(readme_content)
    guide_html = markdown.markdown(guide_content)
    
    # 创建完整的HTML文档
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>AI Travel Planner - 作业提交文档</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }}
            h1, h2, h3 {{
                color: #333;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            code {{
                font-family: Consolas, Monaco, monospace;
            }}
        </style>
    </head>
    <body>
        <h1>AI Travel Planner</h1>
        <h2>GitHub仓库地址</h2>
        <p>https://github.com/your-username/ai-travel-planner</p>
        
        <h2>README文档</h2>
        {readme_html}
        
        <h2>作业提交指南</h2>
        {guide_html}
    </body>
    </html>
    """
    
    # 保存HTML文件
    with open('submission.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("已生成 submission.html 文件")

if __name__ == "__main__":
    generate_pdf()