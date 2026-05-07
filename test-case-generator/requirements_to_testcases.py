#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
需求文档转测试用例生成器
将doc/docx格式的需求文档转换为xlsx格式的测试用例
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import re

try:
    from docx import Document
except ImportError:
    print("需要安装 python-docx: pip install python-docx")
    sys.exit(1)

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
except ImportError:
    print("需要安装 openpyxl: pip install openpyxl")
    sys.exit(1)


class RequirementParser:
    """需求文档解析器"""
    
    def __init__(self, doc_path: str):
        """
        初始化解析器
        
        Args:
            doc_path: doc/docx文件路径
        """
        self.doc_path = doc_path
        self.requirements = []
        self.document = None
        
    def parse(self) -> List[Dict[str, str]]:
        """
        解析需求文档
        
        Returns:
            需求列表，每个需求包含id、标题、描述等信息
        """
        try:
            self.document = Document(self.doc_path)
        except Exception as e:
            print(f"错误：无法打开文档 {self.doc_path}")
            print(f"详情：{e}")
            return []
        
        # 提取文本内容
        full_text = self._extract_text()
        
        # 解析需求
        self.requirements = self._parse_requirements(full_text)
        
        return self.requirements
    
    def _extract_text(self) -> str:
        """
        从document对象中提取所有文本
        
        Returns:
            合并后的文本内容
        """
        text_parts = []
        for paragraph in self.document.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)
        
        # 处理表格中的文本
        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        text_parts.append(cell.text)
        
        return "\n".join(text_parts)
    
    def _parse_requirements(self, text: str) -> List[Dict[str, str]]:
        """
        解析需求文本
        
        Args:
            text: 文档文本内容
            
        Returns:
            需求列表
        """
        requirements = []
        
        # 按行分割
        lines = text.split('\n')
        
        # 尝试识别需求项（支持多种格式）
        current_requirement = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 识别需求标题（以"需求"、"功能"、"FR"等开头）
            if any(keyword in line for keyword in ['需求', '功能', '函数', 'FR', 'Requirement']):
                if current_requirement:
                    requirements.append(current_requirement)
                
                current_requirement = {
                    'title': line,
                    'description': '',
                    'precondition': '系统正常运行',
                    'steps': [],
                    'expected_result': ''
                }
            elif current_requirement:
                # 识别描述、前置条件、步骤、预期结果等
                if any(keyword in line for keyword in ['描述', '说明', 'Description']):
                    current_requirement['description'] = line
                elif any(keyword in line for keyword in ['前置条件', 'Precondition', '前提']):
                    current_requirement['precondition'] = line
                elif any(keyword in line for keyword in ['步骤', '操作', 'Step', 'Action']):
                    current_requirement['steps'].append(line)
                elif any(keyword in line for keyword in ['预期', '结果', 'Expected', 'Result']):
                    current_requirement['expected_result'] = line
                else:
                    # 作为描述的一部分
                    if current_requirement['description']:
                        current_requirement['description'] += '\n' + line
                    else:
                        current_requirement['description'] = line
        
        # 添加最后一个需求
        if current_requirement:
            requirements.append(current_requirement)
        
        return requirements


class TestCaseGenerator:
    """测试用例生成器"""
    
    def __init__(self, requirements: List[Dict[str, str]]):
        """
        初始化生成器
        
        Args:
            requirements: 需求列表
        """
        self.requirements = requirements
        self.test_cases = []
        
    def generate(self) -> List[Dict[str, str]]:
        """
        根据需求生成测试用例
        
        Returns:
            测试用例列表
        """
        for idx, req in enumerate(self.requirements, 1):
            # 为每个需求生成多个测试用例
            test_cases = self._generate_cases_for_requirement(idx, req)
            self.test_cases.extend(test_cases)
        
        return self.test_cases
    
    def _generate_cases_for_requirement(self, req_id: int, req: Dict[str, str]) -> List[Dict[str, str]]:
        """
        为单个需求生成测试用例
        
        Args:
            req_id: 需求ID
            req: 需求信息
            
        Returns:
            该需求对应的测试用例列表
        """
        cases = []
        
        # 正常场景测试用例
        normal_case = {
            'test_case_id': f'TC_{req_id}_001',
            'requirement_id': f'REQ_{req_id}',
            'title': f'{req["title"]} - 正常流程',
            'description': req['description'] or req['title'],
            'precondition': req['precondition'],
            'steps': '\n'.join(req['steps']) if req['steps'] else '执行对应功能',
            'expected_result': req['expected_result'] or '功能执行成功',
            'priority': 'High',
            'test_type': 'Functional'
        }
        cases.append(normal_case)
        
        # 边界值测试用例
        boundary_case = {
            'test_case_id': f'TC_{req_id}_002',
            'requirement_id': f'REQ_{req_id}',
            'title': f'{req["title"]} - 边界值测试',
            'description': f'{req["description"]}（边界值）',
            'precondition': req['precondition'],
            'steps': '\n'.join(req['steps']) if req['steps'] else '使用边界值执行功能',
            'expected_result': '正确处理边界值情况',
            'priority': 'Medium',
            'test_type': 'Boundary'
        }
        cases.append(boundary_case)
        
        # 异常流程测试用例
        exception_case = {
            'test_case_id': f'TC_{req_id}_003',
            'requirement_id': f'REQ_{req_id}',
            'title': f'{req["title"]} - 异常处理',
            'description': f'{req["description"]}（异常场景）',
            'precondition': req['precondition'],
            'steps': '\n'.join(req['steps']) if req['steps'] else '在异常条件下执行功能',
            'expected_result': '系统正确处理异常，给出错误提示',
            'priority': 'Medium',
            'test_type': 'Exception'
        }
        cases.append(exception_case)
        
        return cases


class ExcelExporter:
    """Excel导出器"""
    
    # 定义列头和宽度
    COLUMNS = {
        'test_case_id': ('测试用例ID', 12),
        'requirement_id': ('需求ID', 12),
        'title': ('测试用例标题', 25),
        'description': ('用例描述', 20),
        'precondition': ('前置条件', 20),
        'steps': ('测试步骤', 30),
        'expected_result': ('预期结果', 30),
        'priority': ('优先级', 10),
        'test_type': ('测试类型', 12)
    }
    
    def __init__(self, test_cases: List[Dict[str, str]], output_path: str):
        """
        初始化导出器
        
        Args:
            test_cases: 测试用例列表
            output_path: 输出文件路径
        """
        self.test_cases = test_cases
        self.output_path = output_path
        self.workbook = None
        self.worksheet = None
        
    def export(self) -> bool:
        """
        导出测试用例到Excel
        
        Returns:
            是否导出成功
        """
        try:
            self.workbook = openpyxl.Workbook()
            self.worksheet = self.workbook.active
            self.worksheet.title = '测试用例'
            
            # 写入表头
            self._write_headers()
            
            # 写入数据
            self._write_data()
            
            # 调整列宽和行高
            self._adjust_format()
            
            # 保存文件
            self.workbook.save(self.output_path)
            print(f"✓ 测试用例已成功导出到: {self.output_path}")
            return True
            
        except Exception as e:
            print(f"✗ 导出Excel失败: {e}")
            return False
    
    def _write_headers(self):
        """写入表头"""
        # 定义样式
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF', size=11)
        header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        for col_idx, (key, (label, width)) in enumerate(self.COLUMNS.items(), 1):
            cell = self.worksheet.cell(row=1, column=col_idx)
            cell.value = label
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment
            cell.border = border
            self.worksheet.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = width
        
        # 冻结表头
        self.worksheet.freeze_panes = 'A2'
    
    def _write_data(self):
        """写入测试用例数据"""
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        for row_idx, test_case in enumerate(self.test_cases, 2):
            for col_idx, key in enumerate(self.COLUMNS.keys(), 1):
                cell = self.worksheet.cell(row=row_idx, column=col_idx)
                cell.value = test_case.get(key, '')
                cell.border = border
                cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
                
                # 设置行高
                if test_case.get(key, ''):
                    line_count = str(test_case.get(key, '')).count('\n') + 1
                    self.worksheet.row_dimensions[row_idx].height = max(20, line_count * 15)
    
    def _adjust_format(self):
        """调整格式"""
        # 为所有有内容的行设置对齐方式
        for row in self.worksheet.iter_rows():
            for cell in row:
                if cell.value:
                    cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)


class TestCaseGeneratorApp:
    """测试用例生成应用主类"""
    
    def __init__(self):
        self.parser = None
        self.generator = None
        self.exporter = None
        
    def run(self, input_doc: str, output_excel: str = None) -> bool:
        """
        执行转换流程
        
        Args:
            input_doc: 输入的doc/docx文件路径
            output_excel: 输出的xlsx文件路径（如果为None则自动生成）
            
        Returns:
            是否执行成功
        """
        # 验证输入文件
        if not os.path.exists(input_doc):
            print(f"✗ 错误：文件不存在 - {input_doc}")
            return False
        
        if not input_doc.lower().endswith(('.doc', '.docx')):
            print(f"✗ 错误：不支持的文件格式，请使用doc或docx文件")
            return False
        
        # 确定输出文件路径
        if output_excel is None:
            base_name = Path(input_doc).stem
            output_excel = f"{base_name}_测试用例.xlsx"
        
        print(f"\n{'='*60}")
        print(f"需求文档转测试用例生成器")
        print(f"{'='*60}")
        print(f"输入文件: {input_doc}")
        print(f"输出文件: {output_excel}")
        print(f"{'='*60}\n")
        
        # 1. 解析需求文档
        print("1️⃣  解析需求文档...")
        self.parser = RequirementParser(input_doc)
        requirements = self.parser.parse()
        
        if not requirements:
            print("✗ 未能识别到需求内容")
            return False
        
        print(f"✓ 识别到 {len(requirements)} 个需求")
        for i, req in enumerate(requirements, 1):
            print(f"   {i}. {req['title'][:50]}")
        
        # 2. 生成测试用例
        print("\n2️⃣  生成测试用例...")
        self.generator = TestCaseGenerator(requirements)
        test_cases = self.generator.generate()
        
        print(f"✓ 生成了 {len(test_cases)} 个测试用例")
        
        # 3. 导出到Excel
        print("\n3️⃣  导出到Excel...")
        self.exporter = ExcelExporter(test_cases, output_excel)
        success = self.exporter.export()
        
        if success:
            print(f"\n{'='*60}")
            print("✅ 转换完成！")
            print(f"{'='*60}\n")
        
        return success


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='将需求文档(doc/docx)转换为测试用例(xlsx)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python requirements_to_testcases.py requirements.docx
  python requirements_to_testcases.py requirements.docx -o test_cases.xlsx
        """
    )
    
    parser.add_argument('input', help='输入的需求文档(doc或docx格式)')
    parser.add_argument('-o', '--output', help='输出的Excel文件路径(可选，默认自动生成)', 
                       default=None)
    
    args = parser.parse_args()
    
    # 运行应用
    app = TestCaseGeneratorApp()
    success = app.run(args.input, args.output)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
