import os
import pandas as pd

def batch_rename_with_format():
    current_dir = os.getcwd()
    print(f"--- 增强版：自定义格式命名工具 ---")

    # 1. 获取路径
    excel_name = input("1. 请输入Excel文件名 (如 list.xlsx): ").strip()
    folder_name = input("2. 请输入存放文件的文件夹名 (如 files): ").strip()
    
    excel_path = os.path.join(current_dir, excel_name)
    target_folder = os.path.join(current_dir, folder_name)

    if not os.path.exists(excel_path) or not os.path.exists(target_folder):
        print("❌ 路径错误，请检查文件名或文件夹名！")
        return

    # 2. 读取 Excel
    try:
        df = pd.read_excel(excel_path)
        # 打印列名，方便用户查看
        print(f"\n检测到 Excel 列名: {list(df.columns)}")
        
        # 3. 设置命名格式
        print("\n命名规则说明：使用 {列名} 来代表该列数据")
        print("例子：2026_{姓名}_{学号}")
        fmt = input("请输入命名格式规则: ").strip()

        # 4. 遍历并重命名
        success_count = 0
        # 我们以 Excel 行为主导，这样可以处理“原本文件名不规则”的情况
        # 假设 Excel 第一列永远是“旧文件名”
        old_name_col = df.columns[0] 

        for _, row in df.iterrows():
            old_name_raw = str(row[old_name_col])
            
            # 根据规则生成新名字
            try:
                # 这一行是魔法所在：它会自动把 fmt 里的 {列名} 替换为对应的值
                new_base_name = fmt.format(**row.to_dict())
            except KeyError as e:
                print(f"❌ 格式错误：Excel 中找不到列名 {e}")
                return

            # 在文件夹中寻找匹配的文件
            for filename in os.listdir(target_folder):
                name_part, ext = os.path.splitext(filename)
                
                if name_part == old_name_raw:
                    old_path = os.path.join(target_folder, filename)
                    new_path = os.path.join(target_folder, new_base_name + ext)
                    
                    # 防止目标文件名已存在导致报错
                    if os.path.exists(new_path):
                        print(f"⚠️ 跳过：{new_base_name} 已存在")
                        continue

                    os.rename(old_path, new_path)
                    print(f"✅ 已改名: {filename} -> {new_base_name + ext}")
                    success_count += 1
        
        print(f"\n任务完成！成功处理 {success_count} 个文件。")

    except Exception as e:
        print(f"⚠️ 发生错误: {e}")

if __name__ == "__main__":
    batch_rename_with_format()
