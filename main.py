import os
import pandas as pd

def batch_rename():
    # 打印当前位置，方便调试
    current_dir = os.getcwd()
    print(f"--- 自动重命名工具已启动 ---")
    print(f"当前所在路径: {current_dir}")
    print("-" * 30)

    # 1. 输入信息
    excel_name = input("1. 请输入Excel文件名 (如 list.xlsx): ").strip()
    folder_name = input("2. 请输入存放文件的文件夹名 (如 files): ").strip()

    # 2. 拼接完整路径
    excel_path = os.path.join(current_dir, excel_name)
    target_folder = os.path.join(current_dir, folder_name)

    # 3. 校验路径是否存在
    if not os.path.exists(excel_path):
        print(f"❌ 错误：在当前目录下找不到文件 '{excel_name}'")
        return
    if not os.path.exists(target_folder):
        print(f"❌ 错误：在当前目录下找不到文件夹 '{folder_name}'")
        return

    try:
        # 4. 读取数据 (使用 iloc 避免依赖特定的表头名称)
        # 假设第一列是旧文件名，第二列是新文件名
        df = pd.read_excel(excel_path)
        rename_map = dict(zip(df.iloc[:, 0].astype(str), df.iloc[:, 1].astype(str)))

        # 5. 执行重命名
        success_count = 0
        for filename in os.listdir(target_folder):
            # 分离文件名和后缀（如 "101" 和 ".pdf"）
            name_part, ext = os.path.splitext(filename)
            
            if name_part in rename_map:
                new_base_name = rename_map[name_part]
                old_path = os.path.join(target_folder, filename)
                new_path = os.path.join(target_folder, new_base_name + ext)
                
                # 执行系统重命名操作
                os.rename(old_path, new_path)
                print(f"✅ 已改名: {filename} -> {new_base_name + ext}")
                success_count += 1
        
        print("-" * 30)
        print(f"任务完成！成功处理 {success_count} 个文件。")

    except Exception as e:
        print(f"⚠️ 发生错误: {e}")

if __name__ == "__main__":
    batch_rename()